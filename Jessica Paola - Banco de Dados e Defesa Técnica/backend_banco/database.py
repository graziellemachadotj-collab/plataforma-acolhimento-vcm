"""
Conexão com o banco de dados.

- Sem configuração nenhuma, usa SQLite (um arquivo plataforma.db), que funciona em qualquer
  computador sem instalar nada. Bom para aula e testes.
- Com a variável de ambiente DATABASE_URL apontando para um PostgreSQL com PostGIS, usa a
  versão de produção, com a coluna geográfica GEOGRAPHY(Point, 4326) e o índice GiST.

  Exemplo: DATABASE_URL=postgresql+psycopg://usuario:senha@localhost:5432/plataforma
"""
import os
from pathlib import Path

from sqlalchemy import create_engine, event, text
from sqlalchemy.orm import DeclarativeBase, sessionmaker

PASTA = Path(__file__).resolve().parent
URL_PADRAO = "sqlite:///" + str((PASTA.parent / "plataforma.db").as_posix())


class Base(DeclarativeBase):
    pass


def criar_engine(url: str | None = None):
    url = url or os.environ.get("DATABASE_URL") or URL_PADRAO
    if url.startswith("sqlite"):
        engine = create_engine(url, connect_args={"check_same_thread": False})

        @event.listens_for(engine, "connect")
        def _fk_on(conn, _):  # SQLite só respeita chaves estrangeiras com este pragma
            conn.execute("PRAGMA foreign_keys=ON")

        return engine
    return create_engine(url, pool_pre_ping=True)


engine = criar_engine()
SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)


def usa_postgis(eng=None) -> bool:
    return (eng or engine).dialect.name == "postgresql"


def preparar_postgis(eng) -> None:
    """Ativa o PostGIS e cria a coluna geográfica + índice GiST em services."""
    with eng.begin() as c:
        c.execute(text("CREATE EXTENSION IF NOT EXISTS postgis"))
        c.execute(text(
            "ALTER TABLE services ADD COLUMN IF NOT EXISTS location geography(Point, 4326) "
            "GENERATED ALWAYS AS (ST_SetSRID(ST_MakePoint(longitude, latitude), 4326)::geography) STORED"
        ))
        c.execute(text("CREATE INDEX IF NOT EXISTS services_location_gix ON services USING GIST (location)"))


def iniciar_banco(eng=None, com_exemplos: bool = True) -> None:
    """Cria as tabelas (se não existirem) e carrega os dados iniciais."""
    from . import models  # noqa: F401  (registra as tabelas)
    from .seed import carregar_dados_iniciais

    eng = eng or engine
    Base.metadata.create_all(eng)
    if usa_postgis(eng):
        preparar_postgis(eng)
    with sessionmaker(bind=eng)() as s:
        carregar_dados_iniciais(s, com_exemplos=com_exemplos)
