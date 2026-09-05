import pandas as pd
from config import DATABASE_URL
from sqlalchemy import create_engine, text


def get_db_engine():
    return create_engine(DATABASE_URL)


def atualizar_dimensao_acao(df_dim: pd.DataFrame):
    """Insere novos tickers na dbo.dim_acao se ainda não existirem."""
    if df_dim.empty:
        return

    engine = get_db_engine()

    with engine.connect() as conn:
        res = conn.execute(text("SELECT ticker FROM dbo.dim_acao"))
        tickers_existentes = {row[0] for row in res.fetchall()}

    df_novos = df_dim[~df_dim["ticker"].isin(tickers_existentes)].copy()

    if not df_novos.empty:
        print(
            f"Inserindo {len(df_novos)} novo(s) ticker(s) na dbo.dim_acao..."
        )
        df_novos.to_sql(
            name="dim_acao",
            con=engine,
            if_exists="append",
            index=False,
            schema="dbo",
        )
    else:
        print("Dimensão dim_acao já está atualizada.")


def obter_cotacoes_existentes() -> set:
    """Retorna um conjunto de tuplas (ticker, data_referencia) que já foram inseridos na fato."""
    engine = get_db_engine()
    query = text(
        "SELECT DISTINCT ticker, CONVERT(VARCHAR(10), data_referencia, 120) FROM dbo.fato_cotacao_acao"
    )

    with engine.connect() as conn:
        res = conn.execute(query)
        # Retorna conjunto no formato {('PETR4.SA', '2026-09-04'), ...}
        return {(row[0], str(row[1])) for row in res.fetchall()}


def carregar_fato_acao(df_fato: pd.DataFrame):
    """Realiza a carga incremental de cotações na fato_cotacao_acao."""
    if df_fato.empty:
        print("Nenhum dado para carregar na fato.")
        return

    # Busca registros já gravados para evitar duplicatas
    registros_no_banco = obter_cotacoes_existentes()

    # Filtra mantendo apenas tuplas (ticker, data_referencia) inéditas
    df_novos = df_fato[
        ~df_fato.set_index(["ticker", "data_referencia"]).index.isin(
            registros_no_banco
        )
    ].copy()

    if df_novos.empty:
        print(
            "ℹ️  Todas as cotações extraídas já existem no Azure SQL. Nenhuma carga executada."
        )
        return

    print(
        f"Inserindo {len(df_novos)} cotação(ões) nova(s) na dbo.fato_cotacao_acao..."
    )
    engine = get_db_engine()

    df_novos.to_sql(
        name="fato_cotacao_acao",
        con=engine,
        if_exists="append",
        index=False,
        schema="dbo",
        chunksize=1000,
    )

    print("✅ Carga incremental concluída com sucesso!")