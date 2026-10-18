"""Testes do banco de dados. Rodar:  python -m pytest -q   (dentro da pasta da Jessica)"""
import os
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
os.environ.setdefault("CHAVE_DADOS", "u0b2m8W3TQkq0b6zbyQq8m1mE0n9H9lK1Yy8c3rJm9o=")

from sqlalchemy import select  # noqa: E402
from sqlalchemy.orm import sessionmaker  # noqa: E402

from backend_banco import seguranca  # noqa: E402
from backend_banco.database import criar_engine, iniciar_banco  # noqa: E402
from backend_banco.models import EvidenceEntry, Service, SupportContact, User  # noqa: E402


def banco_temporario():
    url = os.environ.get("TEST_DATABASE_URL") or "sqlite:///" + (Path(tempfile.mkdtemp()) / "t.db").as_posix()
    eng = criar_engine(url)
    iniciar_banco(eng)
    return eng, sessionmaker(bind=eng)


def test_cria_tabelas_e_dados_iniciais():
    eng, S = banco_temporario()
    with S() as s:
        assert len(s.scalars(select(SupportContact)).all()) == 5
        servicos = s.scalars(select(Service)).all()
        assert servicos and all(x.exemplo and x.telefone is None and x.endereco is None for x in servicos)
    iniciar_banco(eng)  # rodar de novo não duplica nada
    with S() as s:
        assert len(s.scalars(select(SupportContact)).all()) == 5


def test_senha_nunca_guardada():
    h = seguranca.gerar_hash_senha("minha-senha-123")
    assert "minha-senha-123" not in h and h.startswith("scrypt$")
    assert seguranca.conferir_senha("minha-senha-123", h)
    assert not seguranca.conferir_senha("errada", h)


def test_relato_cifrado_no_banco():
    eng, S = banco_temporario()
    with S() as s:
        u = User(apelido="teste", senha_hash=seguranca.gerar_hash_senha("x" * 8), consentimento=True)
        s.add(u)
        s.flush()
        texto = "relato sigiloso"
        s.add(EvidenceEntry(user_id=u.id, relato_cifrado=seguranca.cifrar(texto),
                            hash_integridade=seguranca.hash_integridade(texto)))
        s.commit()
        e = s.scalar(select(EvidenceEntry))
        assert texto.encode() not in e.relato_cifrado          # no banco está ilegível
        assert seguranca.decifrar(e.relato_cifrado) == texto   # com a chave, volta ao original
        assert e.hash_integridade == seguranca.hash_integridade(texto)


def test_localizacao_aproximada():
    assert seguranca.localizacao_aproximada(-23.481234, -46.603456) == (-23.48, -46.6)
    assert seguranca.localizacao_aproximada(None, 1) == (None, None)
