"""
Tabelas do banco (modelo de dados do README da defesa técnica).

Regras de privacidade aplicadas no modelo:
  - users: só um ID pseudônimo, apelido e a senha derivada (scrypt). Sem nome, CPF ou endereço.
  - trusted_contacts e evidence_entries: conteúdo SEMPRE cifrado.
  - emergency_alerts: localização já arredondada (aproximada), nunca a exata.
  - services: o endereço é do SERVIÇO, nunca da usuária.
"""
import uuid
from datetime import datetime, timezone

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, LargeBinary, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .database import Base


def agora() -> datetime:
    return datetime.now(timezone.utc)


def novo_id() -> str:
    return uuid.uuid4().hex


class ServiceType(Base):
    """DEAM, Defensoria, ONG, abrigo, saúde, assistência social..."""
    __tablename__ = "service_types"
    codigo: Mapped[str] = mapped_column(String(30), primary_key=True)
    nome: Mapped[str] = mapped_column(String(120))
    descricao: Mapped[str] = mapped_column(Text, default="")


class Service(Base):
    __tablename__ = "services"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nome: Mapped[str] = mapped_column(String(200))
    service_type: Mapped[str] = mapped_column(ForeignKey("service_types.codigo"), index=True)
    telefone: Mapped[str | None] = mapped_column(String(40), nullable=True)
    site: Mapped[str | None] = mapped_column(String(300), nullable=True)
    endereco: Mapped[str | None] = mapped_column(String(300), nullable=True)
    cidade: Mapped[str] = mapped_column(String(120), default="")
    uf: Mapped[str] = mapped_column(String(2), default="")
    latitude: Mapped[float] = mapped_column(Float)
    longitude: Mapped[float] = mapped_column(Float)
    funciona_24h: Mapped[bool] = mapped_column(Boolean, default=False)
    # Dado de exemplo (didático) ou registro real conferido?
    exemplo: Mapped[bool] = mapped_column(Boolean, default=False)
    # Data da última verificação: telefones e endereços mudam (revisar a cada 3 a 6 meses)
    verificado_em: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    # No PostgreSQL existe ainda a coluna "location" GEOGRAPHY(Point, 4326), criada em database.py

    tipo: Mapped[ServiceType] = relationship()


class SupportContact(Base):
    """Canais oficiais nacionais (180, 190, 192, 100, 188)."""
    __tablename__ = "support_contacts"
    numero: Mapped[str] = mapped_column(String(10), primary_key=True)
    nome: Mapped[str] = mapped_column(String(120))
    descricao: Mapped[str] = mapped_column(Text)
    ordem: Mapped[int] = mapped_column(Integer, default=0)


class User(Base):
    __tablename__ = "users"
    id: Mapped[str] = mapped_column(String(32), primary_key=True, default=novo_id)  # pseudônimo
    apelido: Mapped[str] = mapped_column(String(40), unique=True, index=True)
    senha_hash: Mapped[str] = mapped_column(String(200))  # credencial derivada (scrypt)
    consentimento: Mapped[bool] = mapped_column(Boolean, default=False)
    criado_em: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=agora)
    atualizado_em: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=agora, onupdate=agora)


class SessionToken(Base):
    """Sessões de login. Guardamos só o HASH do token, nunca o token."""
    __tablename__ = "sessions"
    token_hash: Mapped[str] = mapped_column(String(64), primary_key=True)
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    expira_em: Mapped[datetime] = mapped_column(DateTime(timezone=True))


class TrustedContact(Base):
    __tablename__ = "trusted_contacts"
    id: Mapped[str] = mapped_column(String(32), primary_key=True, default=novo_id)
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    nome: Mapped[str] = mapped_column(String(80))           # como ela chama a pessoa (pode ser apelido)
    canal: Mapped[str] = mapped_column(String(20))          # telefone, sms, email...
    contato_cifrado: Mapped[bytes] = mapped_column(LargeBinary)
    consentimento: Mapped[bool] = mapped_column(Boolean, default=False)
    criado_em: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=agora)


class EvidenceEntry(Base):
    """Diário de evidências: relato cifrado + hash de integridade."""
    __tablename__ = "evidence_entries"
    id: Mapped[str] = mapped_column(String(32), primary_key=True, default=novo_id)
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    relato_cifrado: Mapped[bytes] = mapped_column(LargeBinary)
    hash_integridade: Mapped[str] = mapped_column(String(64))  # SHA-256 do relato original
    tipo_violencia: Mapped[str | None] = mapped_column(String(30), nullable=True)
    ocorrido_em: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    criado_em: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=agora)


class EmergencyAlert(Base):
    __tablename__ = "emergency_alerts"
    id: Mapped[str] = mapped_column(String(32), primary_key=True, default=novo_id)
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    latitude_aprox: Mapped[float | None] = mapped_column(Float, nullable=True)
    longitude_aprox: Mapped[float | None] = mapped_column(Float, nullable=True)
    mensagem: Mapped[str] = mapped_column(Text)
    contatos_notificados: Mapped[int] = mapped_column(Integer, default=0)
    criado_em: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=agora)
