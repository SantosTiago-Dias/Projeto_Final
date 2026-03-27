from dotenv import load_dotenv
import cpv_synonyms
import extracao_incremental_contratos 
import database_aux as db
from loguru import logger
import sys

load_dotenv('.env')

def main():
    try:
        connection = db.get_connection()
        if connection:
            db.verify_database_exists()
            extracao_incremental_contratos.main()
    except Exception as e:
        logger.error(f"Erro: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()