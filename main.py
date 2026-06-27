# main.py
from src.ingestion import obtener_datos
from src.transformation import transformar_datos
from src.storage import guardar_parquet
from src.agent import preguntar


def refrescar_datos():
    """Pipeline de datos: descarga, transforma y guarda la TRM."""
    datos = obtener_datos()
    df = transformar_datos(datos)
    ruta = guardar_parquet(df)
    print(f"✅ Datos actualizados: {df.height} registros en {ruta}")


def main():
    refrescar_datos()

    pregunta = " dime cual fue la TRM del 15 de junio del 2026"
    respuesta = preguntar(pregunta)
    print()
    print(f"Pregunta: {pregunta}")
    print(f" {respuesta}")


if __name__ == "__main__":
    main()
