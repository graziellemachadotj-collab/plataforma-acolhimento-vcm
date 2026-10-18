"""
Inicia a API da Plataforma de Acolhimento.

Junta as duas metades do back-end:
  - esta pasta (Dayene): backend_api  -> rotas e consultas
  - pasta da Jessica:    backend_banco -> banco de dados

Uso:  python rodar.py           (abre em http://localhost:8000/docs)
      python rodar.py --porta 8080
"""
import argparse
import os
import sys
import webbrowser
from pathlib import Path

AQUI = Path(__file__).resolve().parent


def achar_pasta_jessica() -> Path:
    if os.environ.get("PASTA_BANCO"):
        return Path(os.environ["PASTA_BANCO"])
    for p in [AQUI, *AQUI.parent.glob("Jessica*")]:
        if (p / "backend_banco").is_dir():
            return p
    sys.exit("Não achei a pasta da Jessica com 'backend_banco'. "
             "Deixe as duas pastas lado a lado ou defina PASTA_BANCO.")


sys.path[:0] = [str(AQUI), str(achar_pasta_jessica())]

if __name__ == "__main__":
    import uvicorn

    ap = argparse.ArgumentParser()
    ap.add_argument("--porta", type=int, default=8000)
    ap.add_argument("--sem-navegador", action="store_true")
    a = ap.parse_args()
    url = f"http://localhost:{a.porta}/docs"
    print(f"\n  Plataforma de Acolhimento · API\n  Documentação: {url}\n  Para parar: Ctrl + C\n")
    if not a.sem_navegador:
        webbrowser.open(url)
    uvicorn.run("backend_api.main:app", host="127.0.0.1", port=a.porta, access_log=False)
