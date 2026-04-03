from dotenv import load_dotenv
import cpv_synonyms
import extracao_incremental_contratos 
import database_aux as db
from loguru import logger
import artigos_synonymos
import tipoContratos_synonymos
import tipoProcedimento_synonymos   
import justificacaoNEscriya
import sys

load_dotenv('.env')

def main():

    #Extração dos dados
    try:
        connection = db.get_connection()
        if connection:
            db.verify_database_exists()
            extracao_incremental_contratos.main()
    except Exception as e:
        logger.error(f"Erro: {e}")
        sys.exit(1)

    #População de dados
    try:
        logger.info("A iniciar população de dados")
        cpv_synonyms.main()
        #artigos_synonymos.main()
        tipoContratos_synonymos.main()
        tipoProcedimento_synonymos.main()
        justificacaoNEscriya.main()
        
    
    except Exception as e:
        logger.error(f"Erro: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()