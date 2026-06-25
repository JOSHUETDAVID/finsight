from pathlib import Path

def guardar_parquet(df, ruta="data/TRM.parquet"):
    Path(ruta).parent.mkdir(parents=True, exist_ok=True)  # crea data/ si no existe
    df.write_parquet(ruta)
    return ruta  # devuelve la ruta, útil para logging
