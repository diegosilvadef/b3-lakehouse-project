import os
from urllib.parse import quote_plus
from dotenv import load_dotenv

load_dotenv()

DB_SERVER = os.getenv("AZURE_SQL_SERVER")
DB_NAME = os.getenv("AZURE_SQL_DATABASE")
DB_USER = os.getenv("AZURE_SQL_USER")
DB_PASSWORD = os.getenv("AZURE_SQL_PASSWORD")

# Garante o formato usuario@servidor para Azure se necessário
if DB_SERVER and "@" not in DB_USER and "database.windows.net" in DB_SERVER:
    server_prefix = DB_SERVER.split(".")[0]
    formatted_user = f"{DB_USER}@{server_prefix}"
else:
    formatted_user = DB_USER

odbc_str = (
    f"Driver={{ODBC Driver 17 for SQL Server}};"
    f"Server=tcp:{DB_SERVER},1433;"
    f"Database={DB_NAME};"
    f"Uid={formatted_user};"
    f"Pwd={DB_PASSWORD};"
    f"Encrypt=yes;"
    f"TrustServerCertificate=no;"
    f"Connection Timeout=30;"
)

DATABASE_URL = f"mssql+pyodbc:///?odbc_connect={quote_plus(odbc_str)}"

# Lista revisada de papéis altamente líquidos e com histórico robusto no yfinance
# Lista 100% validada de ativos altamente líquidos e estáveis no yfinance
TICKERS_B3 = [
    # Bancos e setor financeiro
    "ITUB4.SA",  # Itaú Unibanco
    "BBDC4.SA",  # Bradesco
    "BBAS3.SA",  # Banco do Brasil
    "SANB11.SA", # Santander Brasil
    "BPAC11.SA", # BTG Pactual

    # Petróleo, gás e mineração
    "PETR4.SA",  # Petrobras
    "VALE3.SA",  # Vale
    "PRIO3.SA",  # PRIO
    "CSNA3.SA",  # CSN

    # Consumo, varejo e alimentos
    "ABEV3.SA",  # Ambev
    "RENT3.SA",  # Localiza
    "RADL3.SA",  # Raia Drogasil
    "JBSS32.SA", # JBS N.V. (BDR)

    # Saneamento e energia elétrica
    "WEGE3.SA",  # WEG
    "EGIE3.SA",  # Engie Brasil
    "CMIG4.SA",  # Cemig
    "SBSP3.SA",  # Sabesp

    # Papel e celulose
    "SUZB3.SA",  # Suzano
]
