import polars as pl


def transformar_datos(datos):
    df = pl.DataFrame(datos)
    df = (
        df.lazy()
        .with_columns(
            pl.col("valor").cast(pl.Float64),
            pl.col("vigenciadesde").str.strptime(
                pl.Datetime,
            ),
            pl.col("vigenciahasta").str.strptime(
                pl.Datetime,
            ),
        )
        .select("valor", "vigenciadesde", "vigenciahasta")
        .collect()
    )

    df = df.with_columns(
        pl.col("vigenciadesde").dt.date(), pl.col("vigenciahasta").dt.date()
    )
    return df
