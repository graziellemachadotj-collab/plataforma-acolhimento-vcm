"""
Dados iniciais.

- Tipos de serviço e canais oficiais nacionais: dados reais.
- Serviços locais: são EXEMPLOS DIDÁTICOS (exemplo=True), com nome "Exemplo", sem telefone e
  sem endereço. Seguimos a regra do projeto: nunca inventar telefone ou endereço.
  Antes de publicar, a equipe deve trocar pelos serviços reais, conferidos em fonte oficial
  (ex.: Mapa da Rede de Atendimento do governo), preenchendo "verificado_em".
"""
from sqlalchemy import select
from sqlalchemy.orm import Session

from .models import Service, ServiceType, SupportContact

TIPOS = [
    ("DEAM", "Delegacia de Defesa da Mulher", "Registro de ocorrência e pedido de medida protetiva."),
    ("DEFENSORIA", "Defensoria Pública", "Orientação jurídica gratuita: guarda, pensão, separação, medida protetiva."),
    ("CRAM", "Centro de Referência de Atendimento à Mulher", "Acolhimento psicológico e social."),
    ("CREAS", "CREAS", "Assistência social especializada."),
    ("CASA_MULHER", "Casa da Mulher Brasileira", "Serviços integrados em um só lugar."),
    ("SAUDE", "Serviço de saúde de referência", "Atendimento em caso de violência sexual (até 72 h)."),
    ("ABRIGO", "Casa-abrigo", "Acolhimento sigiloso em risco de morte (acesso pela rede)."),
    ("ONG", "ONG / rede de apoio", "Grupos de apoio e acolhimento comunitário."),
    ("CONSELHO_TUTELAR", "Conselho Tutelar", "Quando há risco para crianças e adolescentes."),
]

CANAIS = [
    ("190", "Polícia Militar", "Emergência e risco imediato.", 1),
    ("180", "Central de Atendimento à Mulher", "Orientação e denúncia. Gratuito, sigiloso, 24 horas.", 2),
    ("192", "SAMU", "Atendimento médico de urgência.", 3),
    ("100", "Disque Direitos Humanos", "Quando há risco para crianças e outras pessoas.", 4),
    ("188", "CVV", "Apoio emocional, 24 horas.", 5),
]

# (nome, tipo, cidade, uf, lat, lon) — pontos aproximados de regiões da Grande São Paulo
EXEMPLOS = [
    ("Exemplo · Delegacia da Mulher — Centro", "DEAM", "São Paulo", "SP", -23.5480, -46.6390),
    ("Exemplo · Delegacia da Mulher — Zona Norte", "DEAM", "São Paulo", "SP", -23.4810, -46.6040),
    ("Exemplo · Delegacia da Mulher — Guarulhos", "DEAM", "Guarulhos", "SP", -23.4630, -46.5330),
    ("Exemplo · Defensoria Pública — Centro", "DEFENSORIA", "São Paulo", "SP", -23.5505, -46.6340),
    ("Exemplo · Defensoria Pública — Guarulhos", "DEFENSORIA", "Guarulhos", "SP", -23.4540, -46.5250),
    ("Exemplo · Centro de Referência da Mulher — Zona Leste", "CRAM", "São Paulo", "SP", -23.5420, -46.4720),
    ("Exemplo · CREAS — Zona Sul", "CREAS", "São Paulo", "SP", -23.6510, -46.7090),
    ("Exemplo · Casa da Mulher Brasileira", "CASA_MULHER", "São Paulo", "SP", -23.5330, -46.6250),
    ("Exemplo · Hospital de referência — Zona Norte", "SAUDE", "São Paulo", "SP", -23.4900, -46.6200),
    ("Exemplo · Rede de apoio comunitária — Tucuruvi", "ONG", "São Paulo", "SP", -23.4800, -46.6030),
    ("Exemplo · Conselho Tutelar — Guarulhos", "CONSELHO_TUTELAR", "Guarulhos", "SP", -23.4680, -46.5400),
]


def carregar_dados_iniciais(s: Session, com_exemplos: bool = True) -> None:
    if not s.scalar(select(ServiceType).limit(1)):
        s.add_all(ServiceType(codigo=c, nome=n, descricao=d) for c, n, d in TIPOS)
    if not s.scalar(select(SupportContact).limit(1)):
        s.add_all(SupportContact(numero=n, nome=nm, descricao=d, ordem=o) for n, nm, d, o in CANAIS)
    s.flush()
    if com_exemplos and not s.scalar(select(Service).limit(1)):
        s.add_all(
            Service(nome=n, service_type=t, cidade=c, uf=uf, latitude=lat, longitude=lon,
                    telefone=None, endereco=None, exemplo=True,
                    funciona_24h=(t == "DEAM"))
            for n, t, c, uf, lat, lon in EXEMPLOS
        )
    s.commit()
