import os
import sys
import tempfile
from pathlib import Path

AQUI = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(AQUI))
for p in [AQUI, *AQUI.parent.glob("Jessica*")]:
    if (p / "backend_banco").is_dir():
        sys.path.insert(0, str(p))
        break

# Banco de teste separado: SQLite temporário (ou TEST_DATABASE_URL para testar no PostgreSQL)
os.environ["DATABASE_URL"] = os.environ.get("TEST_DATABASE_URL") or \
    "sqlite:///" + (Path(tempfile.mkdtemp()) / "teste.db").as_posix()
os.environ.setdefault("CHAVE_DADOS", "u0b2m8W3TQkq0b6zbyQq8m1mE0n9H9lK1Yy8c3rJm9o=")
