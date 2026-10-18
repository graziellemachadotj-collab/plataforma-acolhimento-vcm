"""
Segurança dos dados (privacidade por concepção).

- Senha: scrypt com sal aleatório (biblioteca padrão do Python). A senha nunca é guardada.
- Cifra: Fernet (AES + HMAC) para contatos de confiança e relatos do diário.
  A chave fica FORA do banco: variável de ambiente CHAVE_DADOS ou o arquivo .chave_dados
  (criado na primeira execução). Quem tiver só o banco não consegue ler os relatos.
- Integridade: SHA-256 do relato, para mostrar que o texto não foi alterado depois.
- Localização aproximada: arredonda para ~1 km antes de salvar ou enviar.
"""
import base64
import hashlib
import hmac
import os
import secrets
from pathlib import Path

from cryptography.fernet import Fernet, InvalidToken

ARQ_CHAVE = Path(__file__).resolve().parent.parent / ".chave_dados"

# ---------- senha ----------
_N, _R, _P = 2**14, 8, 1


def gerar_hash_senha(senha: str) -> str:
    sal = secrets.token_bytes(16)
    dk = hashlib.scrypt(senha.encode(), salt=sal, n=_N, r=_R, p=_P, dklen=32)
    return f"scrypt${base64.b64encode(sal).decode()}${base64.b64encode(dk).decode()}"


def conferir_senha(senha: str, guardado: str) -> bool:
    try:
        _, sal_b64, dk_b64 = guardado.split("$")
        sal, dk = base64.b64decode(sal_b64), base64.b64decode(dk_b64)
    except ValueError:
        return False
    teste = hashlib.scrypt(senha.encode(), salt=sal, n=_N, r=_R, p=_P, dklen=32)
    return hmac.compare_digest(teste, dk)


# ---------- tokens de sessão ----------
def novo_token() -> str:
    return secrets.token_urlsafe(32)


def hash_token(token: str) -> str:
    return hashlib.sha256(token.encode()).hexdigest()


# ---------- cifra ----------
_fernet: Fernet | None = None


def _carregar_chave() -> bytes:
    chave = os.environ.get("CHAVE_DADOS")
    if chave:
        return chave.encode()
    if ARQ_CHAVE.exists():
        return ARQ_CHAVE.read_bytes().strip()
    chave = Fernet.generate_key()
    ARQ_CHAVE.write_bytes(chave)
    return chave


def fernet() -> Fernet:
    global _fernet
    if _fernet is None:
        _fernet = Fernet(_carregar_chave())
    return _fernet


def cifrar(texto: str) -> bytes:
    return fernet().encrypt(texto.encode())


def decifrar(dado: bytes) -> str:
    try:
        return fernet().decrypt(dado).decode()
    except InvalidToken:
        return "[não foi possível decifrar: chave diferente]"


def hash_integridade(texto: str) -> str:
    return hashlib.sha256(texto.encode()).hexdigest()


# ---------- localização ----------
def localizacao_aproximada(lat: float | None, lon: float | None, casas: int = 2):
    """2 casas decimais ≈ 1,1 km. Nunca guardamos nem mostramos a coordenada exata."""
    if lat is None or lon is None:
        return None, None
    return round(lat, casas), round(lon, casas)
