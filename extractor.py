import pandas as pd
import yfinance as yf
from config import TICKERS_B3


def extrair_dados_b3(
    tickers: list[str] = TICKERS_B3, period: str = "5d"
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Extrai metadados e histórico de preços de ações da B3 usando yfinance.

    :param period: Período de histórico a buscar (ex: '1d', '5d', '1mo')
    """
    print(f"Iniciando extração via yfinance para {len(tickers)} papéis da B3...")

    dim_list = []
    fato_list = []

    for symbol in tickers:
        try:
            ticker_obj = yf.Ticker(symbol)

            # 1. Extração de Metadados (Dimensão)
            info = ticker_obj.info
            dim_list.append(
                {
                    "ticker": symbol,
                    "nome_empresa": info.get("longName")
                    or info.get("shortName")
                    or symbol,
                    "setor": info.get("sector"),
                    "industria": info.get("industry"),
                    "moeda": info.get("currency", "BRL"),
                }
            )

            # 2. Extração de Cotações (Fato)
            hist = ticker_obj.history(period=period)

            if not hist.empty:
                hist = hist.reset_index()
                for _, row in hist.iterrows():
                    # Formata a data para YYYY-MM-DD
                    data_ref = (
                        row["Date"].strftime("%Y-%m-%d")
                        if hasattr(row["Date"], "strftime")
                        else str(row["Date"])[:10]
                    )

                    fato_list.append(
                        {
                            "ticker": symbol,
                            "preco_abertura": (
                                float(row["Open"])
                                if pd.notna(row["Open"])
                                else None
                            ),
                            "preco_fechamento": float(row["Close"]),
                            "preco_maximo": (
                                float(row["High"])
                                if pd.notna(row["High"])
                                else None
                            ),
                            "preco_minimo": (
                                float(row["Low"])
                                if pd.notna(row["Low"])
                                else None
                            ),
                            "volume_negociado": (
                                int(row["Volume"])
                                if pd.notna(row["Volume"])
                                else 0
                            ),
                            "data_referencia": data_ref,
                        }
                    )
        except Exception as e:
            print(f"⚠️ Erro ao extrair dados do ticker {symbol}: {e}")

    df_dim = pd.DataFrame(dim_list)
    df_fato = pd.DataFrame(fato_list)

    print(
        f"Extração concluída: {len(df_dim)} dimensões e {len(df_fato)} registros de cotações."
    )
    return df_dim, df_fato