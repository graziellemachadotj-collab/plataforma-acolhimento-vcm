"""
Aplicação principal (FastAPI).

Dois modos:
  - LOCAL (padrão): todas as rotas, para estudo e para a defesa técnica.  ->  python rodar.py
  - INTERNET (MODO_PUBLICO=1): só as rotas públicas (busca de serviços, autoavaliação,
    canais de ajuda), aceitando chamadas apenas do site oficial e com limite de pedidos.
    Usado quando a API for publicada na internet.

Documentação interativa:  http://localhost:8000/docs
"""
import hashlib
import logging
import os
import time
from collections import defaultdict, deque
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from backend_banco.database import engine, iniciar_banco, usa_postgis

from . import rotas_protegidas, rotas_publicas

MODO_PUBLICO = os.environ.get("MODO_PUBLICO", "").lower() in ("1", "true", "sim")
SITE_OFICIAL = os.environ.get("SITE_OFICIAL", "https://acolhimento.prof.alvaromjunior.com")
LIMITE_POR_MINUTO = int(os.environ.get("LIMITE_POR_MINUTO", "60"))


@asynccontextmanager
async def ciclo_de_vida(app: FastAPI):
    iniciar_banco()
    yield


app = FastAPI(
    title="Plataforma de Acolhimento · API",
    description=("Back-end seguro, público e anônimo para apoiar mulheres em situação de violência doméstica. "
                 "Orientação sem cadastro; conta opcional só para contatos de confiança, diário de evidências e alertas.\n\n"
                 + ("**Modo internet:** apenas as rotas públicas estão ligadas.\n\n" if MODO_PUBLICO else "")
                 + "**Em perigo agora, ligue 190. Orientação sigilosa 24h: 180.**"),
    version="1.1.0",
    lifespan=ciclo_de_vida,
)

# Quem pode chamar a API pelo navegador.
# Local: qualquer origem (inclusive o index.html aberto direto do computador).
# Internet: só o site oficial. Não usamos cookies; o login vai no cabeçalho Authorization.
origens = [SITE_OFICIAL] if MODO_PUBLICO else ["*"]
app.add_middleware(CORSMiddleware, allow_origins=origens, allow_methods=["GET", "POST", "DELETE"],
                   allow_headers=["Authorization", "Content-Type"])

# Limite de pedidos (só no modo internet). O identificador do visitante vira um hash
# e fica apenas na memória por 1 minuto: nada é gravado em disco ou em log.
_janelas: dict[str, deque] = defaultdict(deque)


def _chave_visitante(request: Request) -> str:
    ip = request.headers.get("cf-connecting-ip") or (request.client.host if request.client else "?")
    return hashlib.sha256(ip.encode()).hexdigest()[:16]


@app.middleware("http")
async def protecoes(request: Request, call_next):
    if MODO_PUBLICO and request.method != "OPTIONS":
        agora = time.monotonic()
        fila = _janelas[_chave_visitante(request)]
        while fila and agora - fila[0] > 60:
            fila.popleft()
        if len(fila) >= LIMITE_POR_MINUTO:
            return JSONResponse({"detail": "Muitos pedidos seguidos. Aguarde um minuto. Em perigo, ligue 190."},
                                status_code=429)
        fila.append(agora)
        if len(_janelas) > 10_000:  # evita crescer sem limite
            _janelas.clear()
    resp = await call_next(request)
    resp.headers["X-Content-Type-Options"] = "nosniff"
    resp.headers["Referrer-Policy"] = "no-referrer"
    resp.headers["X-Frame-Options"] = "DENY"
    resp.headers["Cache-Control"] = "no-store"
    return resp


# Minimizar logs: nada de IP, user-agent ou conteúdo. Só erros técnicos.
logging.getLogger("uvicorn.access").disabled = True

app.include_router(rotas_publicas.router)
if not MODO_PUBLICO:
    # Contas, diário e contatos guardam dados sensíveis: só no modo local (estudo/defesa).
    app.include_router(rotas_protegidas.router)


@app.get("/", tags=["Status"], summary="A API está no ar?")
def status():
    return {"ok": True, "projeto": "Plataforma de Acolhimento, Orientação e Resposta Rápida",
            "modo": "internet (só rotas públicas)" if MODO_PUBLICO else "local (todas as rotas)",
            "banco": "PostgreSQL + PostGIS" if usa_postgis(engine) else "SQLite",
            "documentacao": "/docs", "emergencia": "190", "central_da_mulher": "180"}
