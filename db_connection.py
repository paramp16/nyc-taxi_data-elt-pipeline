import psycopg
import os
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()

if __name__ == "__main__":
    conn = None
    curs = None
    try:
        conn =  psycopg.connect(
            host =os.getenv("PSQL_HOST"),
            user = os.getenv("PSQL_USER"),
            port = os.getenv("PSQL_PORT"),
            dbname = os.getenv("PSQL_DBNAME"),
            password = os.getenv("PSQL_PASSWORD")
        )
        sql_path = Path(__file__).parent/"schema.sql"
        with conn.cursor() as curs:
            with open(sql_path,"r", encoding="utf-8") as file:
                schema_sql = file.read()
                statements = [s.strip() for s in schema_sql.split(";") if s.strip()]
            for statement in statements:
                curs.execute(statement)
        conn.commit()
    except Exception as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
        if curs is not None:
            curs.close()
    print("Schema executed Successfully.")
