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

# Lista fixa dos principais papéis da B3
# Lista ampliada dos principais papéis da B3 (Blue Chips e Mid Caps líquidas)
TICKERS_B3 = [
    # Commodities e Petróleo
    "PETR4.SA",
    "VALE3.SA",
    "PRIO3.SA",
    "CSNA3.SA",
    "SUZB3.SA",
    # Bancos e Financeiro
    "ITUB4.SA",
    "BBDC4.SA",
    "BBAS3.SA",
    "SANB11.SA",
    "BPAC11.SA",
    # Consumo, Varejo e Saúde
    "ABEV3.SA",
    "RENT3.SA",
    "RADL3.SA",
    "JBSS3.SA",
    "MGLU3.SA",
    # Elétricas, Saneamento e Infraestrutura
    "WEGE3.SA",
    "EGIE3.SA",
    "CPLE6.SA",
    "SBSP3.SA",
    "CMIG4.SA",
]