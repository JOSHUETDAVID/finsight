from src.transformation import transformar_datos
import polars as pl

def test_transformar_datos():
    datos_falsos = [
        {"valor": "3500.50", "unidad": "COP",
         "vigenciadesde": "2026-06-15T00:00:00.000",
         "vigenciahasta": "2026-06-15T00:00:00.000"}
    ]
    
    df_transformado = transformar_datos(datos_falsos)
    assert df_transformado["valor"].dtype == pl.Float64
    assert df_transformado["vigenciadesde"].dtype == pl.Date
    assert df_transformado["vigenciahasta"].dtype == pl.Date