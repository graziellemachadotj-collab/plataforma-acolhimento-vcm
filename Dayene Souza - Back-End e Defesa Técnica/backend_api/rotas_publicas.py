"""Rotas públicas: funcionam SEM cadastro e SEM login."""
from fastapi import APIRouter, Depends, Header, HTTPException, Query, Response
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import Session

from backend_banco.models import ServiceType, SupportContact

from .autenticacao import encerrar_sessao, get_db
from .autoavaliacao import PERGUNTAS, avaliar
from .cep import regiao_do_cep
from .consultas import servicos_proximos

router = APIRouter(prefix="/api/v1", tags=["Público (sem cadastro)"])

AVISO_EXEMPLO = ("Serviços marcados com exemplo=true são dados didáticos, sem telefone ou endereço. "
                 "Confirme sempre pelo 180 antes de ir a um local.")


@router.get("/services/nearby", summary="Busca serviços por latitude/longitude, raio e tipo")
def nearby(lat: float = Query(..., ge=-90, le=90), lon: float = Query(..., ge=-180, le=180),
           raio_m: int = Query(20_000, ge=500, le=100_000), tipo: str | None = None,
           limite: int = Query(10, ge=1, le=50), db: Session = Depends(get_db)):
    itens = servicos_proximos(db, lat, lon, raio_m, tipo.upper() if tipo else None, limite)
    return {"total": len(itens), "raio_m": raio_m, "servicos": itens, "aviso": AVISO_EXEMPLO}


@router.get("/services/by-cep", summary="Converte CEP em região e busca serviços (o CEP não é salvo)")
def by_cep(cep: str, raio_m: int = Query(15_000, ge=500, le=100_000), tipo: str | None = None,
           limite: int = Query(10, ge=1, le=50), db: Session = Depends(get_db)):
    reg = regiao_do_cep(cep)
    if not reg:
        raise HTTPException(404, "Não encontramos essa região. Ligue 180 para saber os serviços da sua cidade.")
    itens = servicos_proximos(db, reg["latitude"], reg["longitude"], raio_m, tipo.upper() if tipo else None, limite)
    return {"regiao": reg["regiao"], "aproximado": True, "total": len(itens), "servicos": itens,
            "aviso": AVISO_EXEMPLO, "privacidade": "O CEP foi usado só nesta consulta e não foi guardado."}


@router.get("/services/types", summary="Tipos de serviço da rede de apoio")
def tipos(db: Session = Depends(get_db)):
    return [{"codigo": t.codigo, "nome": t.nome, "descricao": t.descricao}
            for t in db.scalars(select(ServiceType).order_by(ServiceType.nome))]


@router.get("/red-flags/questions", summary="Perguntas da autoavaliação")
def perguntas():
    return [{"id": p["id"], "texto": p["texto"]} for p in PERGUNTAS]


class Respostas(BaseModel):
    respostas: dict[str, bool]


@router.post("/red-flags/evaluate", summary="Avalia as respostas SEM salvar nada")
def evaluate(corpo: Respostas):
    return avaliar(corpo.respostas)


@router.get("/support/contacts", summary="Canais oficiais de atendimento")
def contatos(db: Session = Depends(get_db)):
    return [{"numero": c.numero, "nome": c.nome, "descricao": c.descricao}
            for c in db.scalars(select(SupportContact).order_by(SupportContact.ordem))]


@router.post("/quick-escape", summary="Saída rápida: encerra a sessão e limpa dados temporários")
def quick_escape(response: Response, authorization: str | None = Header(default=None),
                 db: Session = Depends(get_db)):
    encerrada = encerrar_sessao(db, authorization)
    response.headers["Clear-Site-Data"] = '"cache", "storage"'
    return {"sessao_encerrada": encerrada, "redirecionar_para": "https://www.google.com/search?q=previs%C3%A3o+do+tempo",
            "aviso": "Nenhum site consegue apagar o histórico do navegador. Use aba anônima ou um aparelho de confiança."}
