"""Testes do modo internet (MODO_PUBLICO=1): só rotas públicas, CORS só do site, limite de pedidos."""
import importlib
import os

import pytest
from fastapi.testclient import TestClient

SITE = "https://acolhimento.prof.alvaromjunior.com"


@pytest.fixture(scope="module")
def cli():
    os.environ.update(MODO_PUBLICO="1", LIMITE_POR_MINUTO="5", SITE_OFICIAL=SITE)
    import backend_api.main as m
    m = importlib.reload(m)
    with TestClient(m.app) as c:
        yield c
    for k in ("MODO_PUBLICO", "LIMITE_POR_MINUTO", "SITE_OFICIAL"):
        os.environ.pop(k, None)
    importlib.reload(m)


def test_so_rotas_publicas(cli):
    assert "internet" in cli.get("/", headers={"cf-connecting-ip": "1.1.1.1"}).json()["modo"]
    h = {"cf-connecting-ip": "1.1.1.2"}
    assert cli.get("/api/v1/support/contacts", headers=h).status_code == 200
    assert cli.post("/api/v1/auth/register", headers=h,
                    json={"apelido": "x1x", "senha": "senha-forte-123", "consentimento": True}).status_code == 404
    assert cli.get("/api/v1/evidence", headers=h).status_code == 404


def test_cors_so_do_site(cli):
    ok = cli.get("/", headers={"Origin": SITE, "cf-connecting-ip": "2.2.2.1"})
    assert ok.headers.get("access-control-allow-origin") == SITE
    outro = cli.get("/", headers={"Origin": "https://site-qualquer.com", "cf-connecting-ip": "2.2.2.2"})
    assert "access-control-allow-origin" not in outro.headers


def test_limite_de_pedidos(cli):
    h = {"cf-connecting-ip": "3.3.3.3"}
    codigos = [cli.get("/api/v1/support/contacts", headers=h).status_code for _ in range(7)]
    assert codigos[:5] == [200] * 5 and codigos[-1] == 429
    # outro visitante não é afetado
    assert cli.get("/api/v1/support/contacts", headers={"cf-connecting-ip": "4.4.4.4"}).status_code == 200
