import os
from pathlib import Path

import pandas as pd
from dbfread import DBF
from dotenv import load_dotenv
from pysus.online_data.SINAN import download
from sqlalchemy import create_engine

dotenv_path = Path().resolve().parents[1] / ".env"
load_dotenv(dotenv_path=dotenv_path)

db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")
db_name = os.getenv("DB_NAME")


if not all([db_user, db_password, db_host, db_port, db_name]):
    print("Erro: Uma ou mais variáveis de ambiente não foram carregadas.")
    print("Verifique o arquivo .env.")
    exit(1)

# Criar a engine de conexão
engine = create_engine(
    f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
)


years = list(range(2001, 2024))
states = "PE"

for year in years:
    try:
        print(f"Processando o year {year}...")

        download("DENGUE", year, states)

        files_dbf = [file for file in os.listdir(".") if file.endswith(".dbf")]
        if not files_dbf:
            print(f"Nenhum arquivo DBF encontrado para o ano {year}.")
            continue

        for file_dbf in files_dbf:
            print(f"Lendo o arquivo {file_dbf}...")

            records = DBF(file_dbf, encoding="latin-1")
            df = pd.DataFrame(iter(records))

            df["ano"] = year

            print("Inserindo dados no banco de dados...")
            df.to_sql("dengue_todos_os_years", engine, if_exists="append", index=False)

            os.remove(file_dbf)

            print(f"Dados do arquivo {file_dbf} do year {year} inseridos com sucesso.")

    except Exception as e:
        print(f"Erro ao processar o year {year}: {e}")

print("Processamento concluído.")
