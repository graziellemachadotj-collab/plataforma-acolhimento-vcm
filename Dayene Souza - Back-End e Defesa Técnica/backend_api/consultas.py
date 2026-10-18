"""
Consultas de serviços por proximidade (otimização das consultas).

PostgreSQL + PostGIS:
  usa ST_DWithin (filtra pelo raio usando o índice GiST) e ST_Distance (distância real
  em metros sobre a Terra), ordenando do mais próximo para o mais longe.

SQLite (modo de aula):
  1) filtra primeiro por uma "caixa" de latitude/longitude em volta do ponto (barato);
  2) só nesses candidatos calcula a distância real pela fórmula de Haversine.
"""
import math

from sqlalchemy import and_, select, text
from sqlalchemy.orm import Session

from backend_banco.database import usa_postgis
from backend_banco.models import Service

RAIO_TERRA_M = 6_371_000


def haversine_m(lat1, lon1, lat2, lon2) -> float:
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp, dl = p2 - p1, math.radians(lon2 - lon1)
    a = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * RAIO_TERRA_M * math.asin(math.sqrt(a))


def _como_dict(sv: Service, distancia_m: float) -> dict:
    return {
        "id": sv.id, "nome": sv.nome, "tipo": sv.service_type,
        "telefone": sv.telefone, "site": sv.site, "endereco": sv.endereco,
        "cidade": sv.cidade, "uf": sv.uf, "funciona_24h": sv.funciona_24h,
        "distancia_m": round(distancia_m), "exemplo": sv.exemplo,
        "verificado_em": sv.verificado_em.isoformat() if sv.verificado_em else None,
    }


def servicos_proximos(db: Session, lat: float, lon: float, raio_m: int = 20_000,
                      tipo: str | None = None, limite: int = 10) -> list[dict]:
    if usa_postgis(db.get_bind()):
        sql = text("""
            SELECT id, ST_Distance(location, ST_SetSRID(ST_MakePoint(:lon, :lat), 4326)::geography) AS distancia_m
              FROM services
             WHERE (CAST(:tipo AS varchar) IS NULL OR service_type = CAST(:tipo AS varchar))
               AND ST_DWithin(location, ST_SetSRID(ST_MakePoint(:lon, :lat), 4326)::geography, :raio)
             ORDER BY distancia_m
             LIMIT :limite
        """)
        linhas = db.execute(sql, {"lat": lat, "lon": lon, "raio": raio_m, "tipo": tipo, "limite": limite}).all()
        por_id = {s.id: s for s in db.scalars(select(Service).where(Service.id.in_([l.id for l in linhas])))}
        return [_como_dict(por_id[l.id], l.distancia_m) for l in linhas]

    # Caixa em volta do ponto: 1 grau de latitude ≈ 111,32 km
    dlat = raio_m / 111_320
    dlon = raio_m / (111_320 * max(math.cos(math.radians(lat)), 0.01))
    filtro = [Service.latitude.between(lat - dlat, lat + dlat),
              Service.longitude.between(lon - dlon, lon + dlon)]
    if tipo:
        filtro.append(Service.service_type == tipo)
    candidatos = db.scalars(select(Service).where(and_(*filtro))).all()
    com_dist = [(s, haversine_m(lat, lon, s.latitude, s.longitude)) for s in candidatos]
    com_dist = sorted((x for x in com_dist if x[1] <= raio_m), key=lambda x: x[1])[:limite]
    return [_como_dict(s, d) for s, d in com_dist]
