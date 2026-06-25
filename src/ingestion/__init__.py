import httpx
from time import sleep


def obtener_datos(limite=1000, reintentos=5):
    url = f"https://www.datos.gov.co/resource/32sa-8pi3.json?$limit={limite}"

    for intento in range(reintentos):
        try:
            response = httpx.get(url, timeout=10)
            response.raise_for_status()  # ← (1) ¿qué método lanza si hay error HTTP?
            datos = response.json()

            if not datos:  # ← (2) ¿cómo detectas lista vacía?
                raise ValueError("Respuesta vacía")

            return datos  # único punto de éxito

        except (
            httpx.HTTPStatusError,
            httpx.TimeoutException,
            httpx.RequestError,
            ValueError,
        ) as e:
            if intento == reintentos - 1:  # último intento
                raise  # ← (3) ¿qué haces? (no es print)
            espera = 2**intento  # ← (4) backoff que crece con intento
            print(f"Intento {intento + 1} falló: {e}. Reintento en {espera}s")
            sleep(espera)
