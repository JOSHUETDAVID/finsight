import psycopg
import os
from dotenv import load_dotenv

load_dotenv()

URL = os.getenv("DATABASE_URL")

TABLA = """
CREATE TABLE IF NOT EXISTS trm (
    vigenciadesde DATE PRIMARY KEY,
    vigenciahasta DATE,
    valor NUMERIC
)
"""

DATOS = """
INSERT INTO trm (vigenciadesde, vigenciahasta, valor)
VALUES (%s, %s, %s)
ON CONFLICT (vigenciadesde) DO NOTHING
"""


def guardar_datos_bd(data):
    if not URL:
        raise RuntimeError("DATABASE_URL no configurada")

    with psycopg.connect(URL) as conn:
        with conn.cursor() as cur:
            cur.execute(TABLA)
            for fila in data:
                cur.execute(
                    DATOS,
                    (
                        fila["vigenciadesde"],
                        fila["vigenciahasta"],
                        fila["valor"],
                    ),
                )
    print(f"Datos guardados: {len(data)} registros")
