from database import atualizar_dimensao_acao, carregar_fato_acao
from extractor import extrair_dados_b3


def run_pipeline():
    print("=== INICIANDO PIPELINE DE COTAÇÕES DA B3 (YFINANCE) ===")

    try:
        # 1. Extração dos dados (com base na lista fixa definida em config.py)
        df_dim, df_fato = extrair_dados_b3(period="1d")

        if df_dim.empty or df_fato.empty:
            print("⚠️  Nenhum dado retornado pela extração.")
            return

        print(f"✅ Extração concluída. Dimensão: {len(df_dim)} registros, Fato: {len(df_fato)} registros.")

        # 2. Atualização da Dimensão (Insere novos tickers se necessário)
        atualizar_dimensao_acao(df_dim)

        # 3. Carga Incremental na Fato (Evita duplicação de cotações já gravadas)
        carregar_fato_acao(df_fato)

        print("=== PIPELINE FINALIZADO COM SUCESSO ===")

    except Exception as e:
        print(f"❌ ERRO DURANTE A EXECUÇÃO DO PIPELINE: {e}")


if __name__ == "__main__":
    run_pipeline()