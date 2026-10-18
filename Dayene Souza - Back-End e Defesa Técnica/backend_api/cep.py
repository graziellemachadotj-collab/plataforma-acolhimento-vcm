"""
CEP -> região aproximada para a busca de serviços.

Cuidados (do prompt do chatbot):
  - o CEP NÃO é salvo nem registrado em log; é usado só durante a consulta;
  - a usuária pode informar um CEP "seguro" (casa de amiga, trabalho);
  - a resposta é o centro aproximado da REGIÃO, não o endereço.

Esta versão funciona sem internet, com as faixas de CEP da Grande São Paulo.
Para o Brasil todo, ligar um serviço de geocodificação oficial nesta função.
"""
import re

# (início, fim da faixa de 5 dígitos, nome da região, lat, lon aproximados)
FAIXAS = [
    (1000, 1599, "São Paulo · Centro", -23.548, -46.636),
    (2000, 2999, "São Paulo · Zona Norte", -23.485, -46.620),
    (3000, 3999, "São Paulo · Zona Leste", -23.545, -46.560),
    (4000, 4999, "São Paulo · Zona Sul", -23.620, -46.660),
    (5000, 5899, "São Paulo · Zona Oeste", -23.560, -46.700),
    (8000, 8499, "São Paulo · Extremo Leste", -23.540, -46.450),
    (7000, 7399, "Guarulhos", -23.462, -46.533),
]


def limpar_cep(cep: str) -> str | None:
    digitos = re.sub(r"\D", "", cep or "")
    return digitos if len(digitos) == 8 else None


def regiao_do_cep(cep: str) -> dict | None:
    d = limpar_cep(cep)
    if not d:
        return None
    prefixo = int(d[:5])
    for ini, fim, nome, lat, lon in FAIXAS:
        if ini <= prefixo <= fim:
            return {"regiao": nome, "latitude": lat, "longitude": lon, "aproximado": True}
    return None
