"""Testes da API. Rodar:  python -m pytest -q   (dentro da pasta da Dayene)"""
import pytest
from fastapi.testclient import TestClient

from backend_api.main import app


@pytest.fixture(scope="module")
def cli():
    with TestClient(app) as c:
        yield c


def entrar(cli, apelido):
    r = cli.post("/api/v1/auth/register", json={"apelido": apelido, "senha": "senha-forte-123", "consentimento": True})
    assert r.status_code == 201, r.text
    return {"Authorization": "Bearer " + r.json()["token"]}


def test_status(cli):
    r = cli.get("/")
    assert r.status_code == 200 and r.json()["ok"]
    assert r.headers["x-content-type-options"] == "nosniff"


def test_busca_por_coordenadas_ordenada(cli):
    # perto do Tucuruvi (zona norte)
    r = cli.get("/api/v1/services/nearby", params={"lat": -23.48, "lon": -46.603, "raio_m": 20000})
    d = r.json()
    assert r.status_code == 200 and d["total"] > 0
    dist = [s["distancia_m"] for s in d["servicos"]]
    assert dist == sorted(dist) and dist[-1] <= 20000
    assert all(s["exemplo"] for s in d["servicos"])


def test_busca_por_tipo(cli):
    d = cli.get("/api/v1/services/nearby", params={"lat": -23.55, "lon": -46.63, "tipo": "deam"}).json()
    assert d["total"] >= 1 and {s["tipo"] for s in d["servicos"]} == {"DEAM"}


def test_raio_pequeno_sem_resultado(cli):
    d = cli.get("/api/v1/services/nearby", params={"lat": -3.1, "lon": -60.0, "raio_m": 1000}).json()
    assert d["total"] == 0


def test_busca_por_cep(cli):
    d = cli.get("/api/v1/services/by-cep", params={"cep": "07010-000"}).json()
    assert d["regiao"] == "Guarulhos" and d["total"] > 0
    assert "não foi guardado" in d["privacidade"]
    assert cli.get("/api/v1/services/by-cep", params={"cep": "123"}).status_code == 404


def test_autoavaliacao_sem_persistencia(cli):
    qs = cli.get("/api/v1/red-flags/questions").json()
    assert len(qs) == 12
    alto = cli.post("/api/v1/red-flags/evaluate", json={"respostas": {"ameaca_morte": True, "controle": True}}).json()
    assert alto["nivel"] == "alto" and "190" in alto["mensagem"]
    nada = cli.post("/api/v1/red-flags/evaluate", json={"respostas": {}}).json()
    assert nada["nivel"] == "sem_sinais"


def test_canais_oficiais(cli):
    nums = [c["numero"] for c in cli.get("/api/v1/support/contacts").json()]
    assert nums[:2] == ["190", "180"] and {"192", "100", "188"} <= set(nums)


def test_rotas_protegidas_exigem_login(cli):
    assert cli.get("/api/v1/evidence").status_code == 401
    assert cli.get("/api/v1/trusted-contacts", headers={"Authorization": "Bearer invalido"}).status_code == 401


def test_cadastro_login_e_senha_errada(cli):
    entrar(cli, "girassol")
    assert cli.post("/api/v1/auth/register", json={"apelido": "girassol", "senha": "outra-senha-1", "consentimento": True}).status_code == 409
    assert cli.post("/api/v1/auth/login", json={"apelido": "girassol", "senha": "errada-123"}).status_code == 401
    assert cli.post("/api/v1/auth/login", json={"apelido": "girassol", "senha": "senha-forte-123"}).status_code == 200
    assert cli.post("/api/v1/auth/register", json={"apelido": "semconsent", "senha": "senha-forte-123", "consentimento": False}).status_code == 400


def test_contatos_diario_e_alerta(cli):
    h = entrar(cli, "lua")
    c = cli.post("/api/v1/trusted-contacts", headers=h,
                 json={"nome": "Irmã", "canal": "telefone", "contato": "11 90000-0000", "consentimento": True})
    assert c.status_code == 201 and c.json()["contato"] == "11 90000-0000"

    e = cli.post("/api/v1/evidence", headers=h, json={"relato": "Ele quebrou meu celular.", "tipo_violencia": "patrimonial"})
    assert e.status_code == 201 and e.json()["integro"]
    reg = cli.get("/api/v1/evidence", headers=h).json()["registros"]
    assert len(reg) == 1 and reg[0]["relato"] == "Ele quebrou meu celular."

    a = cli.post("/api/v1/emergency-alerts", headers=h,
                 json={"consentimento": True, "latitude": -23.481234, "longitude": -46.603456})
    d = a.json()
    assert a.status_code == 201 and d["localizacao_aproximada"] == {"lat": -23.48, "lon": -46.6}
    assert len(d["destinatarios"]) == 1
    assert cli.post("/api/v1/emergency-alerts", headers=h, json={"consentimento": False}).status_code == 400


def test_isolamento_entre_contas(cli):
    h1, h2 = entrar(cli, "estrela"), entrar(cli, "mar")
    eid = cli.post("/api/v1/evidence", headers=h1, json={"relato": "registro privado"}).json()["id"]
    assert cli.get("/api/v1/evidence", headers=h2).json()["registros"] == []
    assert cli.delete(f"/api/v1/evidence/{eid}", headers=h2).status_code == 404


def test_saida_rapida_encerra_sessao(cli):
    h = entrar(cli, "flor")
    r = cli.post("/api/v1/quick-escape", headers=h)
    assert r.json()["sessao_encerrada"] and "Clear-Site-Data" in r.headers
    assert cli.get("/api/v1/evidence", headers=h).status_code == 401


def test_excluir_conta(cli):
    h = entrar(cli, "nuvem")
    cli.post("/api/v1/evidence", headers=h, json={"relato": "x"})
    assert cli.delete("/api/v1/auth/account", headers=h).json()["excluida"]
    assert cli.post("/api/v1/auth/login", json={"apelido": "nuvem", "senha": "senha-forte-123"}).status_code == 401
