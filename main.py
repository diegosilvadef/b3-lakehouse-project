from database import atualizar_dimensao_acao, carregar_fato_acao
from extractor import extrair_dados_b3


def run_pipeline():
    print("=== INICIANDO PIPELINE DE COTAÇÕES DA B3 (YFINANCE) ===")

    try:
        # 1. Extração (Pega os últimos x dias úteis)
        df_dim, df_fato = extrair_dados_b3(period="1d")

        # print(df_dim.head(5))
        # print("--------------------------------")
        # print(df_fato.head(5))

        # 2. Atualização da Dimensão
        atualizar_dimensao_acao(df_dim)

        # 3. Carga Incremental na Fato
        carregar_fato_acao(df_fato)

        print("=== PIPELINE FINALIZADO COM SUCESSO ===")

    except Exception as e:
        print(f"❌ ERRO DURANTE A EXECUÇÃO DO PIPELINE: {e}")


if __name__ == "__main__":
    run_pipeline()