"""
Rotas protegidas: só com conta OPCIONAL.
Contatos de confiança, diário de evidências e alertas consentidos.
"""
from datetime import datetime

from fastapi import APIRouter, Depends, Header, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from backend_banco.models import EmergencyAlert, EvidenceEntry, TrustedContact, User
from backend_banco.seguranca import (cifrar, conferir_senha, decifrar, gerar_hash_senha,
                                     hash_integridade, localizacao_aproximada)

from .autenticacao import criar_sessao, encerrar_sessao, get_db, usuaria_logada

router = APIRouter(prefix="/api/v1", tags=["Protegido (conta opcional)"])


# ---------------- autenticação ----------------
class Cadastro(BaseModel):
    apelido: str = Field(min_length=3, max_length=40, description="Não use seu nome verdadeiro")
    senha: str = Field(min_length=8, max_length=128)
    consentimento: bool = Field(description="Concorda em guardar dados protegidos nesta conta")


class Login(BaseModel):
    apelido: str
    senha: str


@router.post("/auth/register", status_code=201, summary="Cadastro opcional (coleta mínima)")
def register(c: Cadastro, db: Session = Depends(get_db)):
    if not c.consentimento:
        raise HTTPException(400, "A conta só é criada com o seu consentimento.")
    u = User(apelido=c.apelido.strip().lower(), senha_hash=gerar_hash_senha(c.senha), consentimento=True)
    db.add(u)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(409, "Esse apelido já existe. Escolha outro.")
    return {"id": u.id, "apelido": u.apelido, "token": criar_sessao(db, u)}


@router.post("/auth/login", summary="Autenticação")
def login(c: Login, db: Session = Depends(get_db)):
    u = db.scalar(select(User).where(User.apelido == c.apelido.strip().lower()))
    if not u or not conferir_senha(c.senha, u.senha_hash):  # mesma mensagem: não revela se o apelido existe
        raise HTTPException(401, "Apelido ou senha incorretos.")
    return {"token": criar_sessao(db, u)}


@router.post("/auth/logout", summary="Sair da conta")
def logout(authorization: str | None = Header(default=None), db: Session = Depends(get_db)):
    return {"sessao_encerrada": encerrar_sessao(db, authorization)}


@router.delete("/auth/account", summary="Excluir a conta e TODOS os dados dela")
def excluir_conta(u: User = Depends(usuaria_logada), db: Session = Depends(get_db)):
    for modelo in (TrustedContact, EvidenceEntry, EmergencyAlert):
        for item in db.scalars(select(modelo).where(modelo.user_id == u.id)):
            db.delete(item)
    db.delete(u)
    db.commit()
    return {"excluida": True}


# ---------------- contatos de confiança ----------------
class NovoContato(BaseModel):
    nome: str = Field(min_length=1, max_length=80)
    canal: str = Field(pattern="^(telefone|sms|whatsapp|email)$")
    contato: str = Field(min_length=3, max_length=120)
    consentimento: bool = Field(description="A pessoa sabe e concorda em ser contato de confiança")


def _contato_dict(c: TrustedContact) -> dict:
    return {"id": c.id, "nome": c.nome, "canal": c.canal, "contato": decifrar(c.contato_cifrado),
            "consentimento": c.consentimento, "criado_em": c.criado_em.isoformat()}


@router.post("/trusted-contacts", status_code=201, summary="Cadastrar contato de confiança (cifrado)")
def add_contato(c: NovoContato, u: User = Depends(usuaria_logada), db: Session = Depends(get_db)):
    item = TrustedContact(user_id=u.id, nome=c.nome, canal=c.canal,
                          contato_cifrado=cifrar(c.contato), consentimento=c.consentimento)
    db.add(item)
    db.commit()
    return _contato_dict(item)


@router.get("/trusted-contacts", summary="Listar contatos de confiança")
def list_contatos(u: User = Depends(usuaria_logada), db: Session = Depends(get_db)):
    return [_contato_dict(c) for c in db.scalars(select(TrustedContact).where(TrustedContact.user_id == u.id))]


@router.delete("/trusted-contacts/{cid}", summary="Remover contato de confiança")
def del_contato(cid: str, u: User = Depends(usuaria_logada), db: Session = Depends(get_db)):
    c = db.get(TrustedContact, cid)
    if not c or c.user_id != u.id:
        raise HTTPException(404, "Contato não encontrado.")
    db.delete(c)
    db.commit()
    return {"removido": True}


# ---------------- diário de evidências ----------------
class NovoRelato(BaseModel):
    relato: str = Field(min_length=1, max_length=20_000)
    tipo_violencia: str | None = Field(default=None, pattern="^(fisica|psicologica|sexual|patrimonial|moral|vicaria)$")
    ocorrido_em: datetime | None = None


def _relato_dict(e: EvidenceEntry) -> dict:
    texto = decifrar(e.relato_cifrado)
    return {"id": e.id, "relato": texto, "tipo_violencia": e.tipo_violencia,
            "ocorrido_em": e.ocorrido_em.isoformat() if e.ocorrido_em else None,
            "criado_em": e.criado_em.isoformat(), "hash_integridade": e.hash_integridade,
            "integro": hash_integridade(texto) == e.hash_integridade}


@router.post("/evidence", status_code=201, summary="Registrar no diário de evidências (cifrado)")
def add_relato(r: NovoRelato, u: User = Depends(usuaria_logada), db: Session = Depends(get_db)):
    e = EvidenceEntry(user_id=u.id, relato_cifrado=cifrar(r.relato), hash_integridade=hash_integridade(r.relato),
                      tipo_violencia=r.tipo_violencia, ocorrido_em=r.ocorrido_em)
    db.add(e)
    db.commit()
    return _relato_dict(e)


@router.get("/evidence", summary="Ler o diário de evidências")
def list_relatos(u: User = Depends(usuaria_logada), db: Session = Depends(get_db)):
    q = select(EvidenceEntry).where(EvidenceEntry.user_id == u.id).order_by(EvidenceEntry.criado_em)
    return {"registros": [_relato_dict(e) for e in db.scalars(q)],
            "aviso": "O diário organiza e preserva seus registros. Ele não substitui orientação jurídica, psicológica ou atendimento de emergência."}


@router.delete("/evidence/{eid}", summary="Apagar um registro do diário")
def del_relato(eid: str, u: User = Depends(usuaria_logada), db: Session = Depends(get_db)):
    e = db.get(EvidenceEntry, eid)
    if not e or e.user_id != u.id:
        raise HTTPException(404, "Registro não encontrado.")
    db.delete(e)
    db.commit()
    return {"removido": True}


# ---------------- alerta de emergência ----------------
class NovoAlerta(BaseModel):
    consentimento: bool = Field(description="Confirma que quer avisar os contatos de confiança")
    latitude: float | None = Field(default=None, ge=-90, le=90)
    longitude: float | None = Field(default=None, ge=-180, le=180)
    mensagem: str = Field(default="Preciso de ajuda. Por favor, entre em contato comigo.", max_length=300)


@router.post("/emergency-alerts", status_code=201, summary="Alerta consentido com localização APROXIMADA")
def alerta(a: NovoAlerta, u: User = Depends(usuaria_logada), db: Session = Depends(get_db)):
    if not a.consentimento:
        raise HTTPException(400, "O alerta só é enviado com a sua confirmação.")
    contatos = db.scalars(select(TrustedContact).where(TrustedContact.user_id == u.id,
                                                       TrustedContact.consentimento.is_(True))).all()
    lat, lon = localizacao_aproximada(a.latitude, a.longitude)
    reg = EmergencyAlert(user_id=u.id, latitude_aprox=lat, longitude_aprox=lon,
                         mensagem=a.mensagem, contatos_notificados=len(contatos))
    db.add(reg)
    db.commit()
    texto = a.mensagem + (f" Região aproximada: https://maps.google.com/?q={lat},{lon}" if lat is not None else "")
    return {
        "id": reg.id, "mensagem_para_enviar": texto, "localizacao_aproximada": {"lat": lat, "lon": lon},
        "destinatarios": [{"nome": c.nome, "canal": c.canal, "contato": decifrar(c.contato_cifrado)} for c in contatos],
        "aviso": "Nesta versão o envio automático (SMS/e-mail) ainda não está ligado: a mensagem fica pronta "
                 "para ela enviar. Em perigo imediato, ligue 190.",
    }
