"""
Login opcional. O token vai no cabeçalho:  Authorization: Bearer <token>
No banco fica só o hash do token (se o banco vazar, os tokens não servem).
"""
from datetime import datetime, timedelta, timezone

from fastapi import Depends, Header, HTTPException
from sqlalchemy.orm import Session

from backend_banco.database import SessionLocal
from backend_banco.models import SessionToken, User
from backend_banco.seguranca import hash_token, novo_token

DURACAO = timedelta(hours=8)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def criar_sessao(db: Session, user: User) -> str:
    token = novo_token()
    db.add(SessionToken(token_hash=hash_token(token), user_id=user.id,
                        expira_em=datetime.now(timezone.utc) + DURACAO))
    db.commit()
    return token


def _token_do_cabecalho(authorization: str | None) -> str | None:
    if authorization and authorization.lower().startswith("bearer "):
        return authorization[7:].strip()
    return None


def encerrar_sessao(db: Session, authorization: str | None) -> bool:
    token = _token_do_cabecalho(authorization)
    if not token:
        return False
    s = db.get(SessionToken, hash_token(token))
    if s:
        db.delete(s)
        db.commit()
        return True
    return False


def usuaria_logada(authorization: str | None = Header(default=None),
                   db: Session = Depends(get_db)) -> User:
    token = _token_do_cabecalho(authorization)
    if not token:
        raise HTTPException(401, "Faça login para usar esta função.")
    s = db.get(SessionToken, hash_token(token))
    expira = s.expira_em if s else None
    if expira is not None and expira.tzinfo is None:  # SQLite devolve sem fuso
        expira = expira.replace(tzinfo=timezone.utc)
    if not s or expira < datetime.now(timezone.utc):
        raise HTTPException(401, "Sessão expirada. Entre novamente.")
    user = db.get(User, s.user_id)
    if not user:
        raise HTTPException(401, "Sessão inválida.")
    return user
