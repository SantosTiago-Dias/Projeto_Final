from dotenv import load_dotenv
import database_aux as db
from loguru import logger
import extracao_incremental_contratos
import sys

#População de dados
import cpv_synonyms
import artigos_synonymos
import tipoContratos_synonymos as contrato_synonymos
import tipoProcedimento_synonymos as procedimento_Synonymos
import justificacaoNEscrita as justificacao
#Fim de população de dados

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

    try:
        db.execute_transformacao()
    except Exception as e:
        logger.error(f"Erro: {e}")
        sys.exit(1)

    #População de dados
    #TODO:Populacionar os dados dps
    try:
        logger.info("A iniciar população de dados")
        cpv_synonyms.main()
        contrato_synonymos.main()
        procedimento_Synonymos.main()
        justificacao.main()
        artigos_synonymos.main()
        logger.info("Fim da população dados")
    
    except Exception as e:
        logger.error(f"Erro: {e}")
        sys.exit(1)

    try:
        db.execute_transformacao()
        db.execute_load()
    except Exception as e:
        logger.error(f"Erro: {e}")
        sys.exit(1)
    


if __name__ == "__main__":
    main()