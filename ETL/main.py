from dotenv import load_dotenv
import database_aux as db
from loguru import logger
import extracao_incremental_contratos
import sys
import Entity_retries
import Notify_laravel

#População de dados
import cpv_synonyms
import artigos_synonymos
import tipoContratos_synonymos as contrato_synonymos
import tipoProcedimento_synonymos as procedimento_Synonymos
import justificacaoNEscrita as justificacao
#Fim de população de dados


def main():

    #region Connection to DB
    connection = db.get_connection()
    if not connection:
        logger.error("Não foi possivel estabelecer uma connecção com a base de dados")
        sys.exit(1)
    #endregion    

    """"
    #region Extração
    try:
        logger.info("A iniciar extração de dados")
        db.drop_staging_tables()
        Entity_retries.main()
        extracao_incremental_contratos.main()
    except Exception as e:
        logger.error(f"Erro: {e}")
        sys.exit(1)
    #endregion
    """
    #region Transformação
    try:
        logger.info("A iniciar transformação de dados")
        db.execute_transformacao()
        db.enrich_entidades_transf()
        logger.success("Fim da transformação de dados")
    except Exception as e:
        logger.error(f"Erro: {e}")
        sys.exit(1)
    #endregion

    #region População de dados
    try:
        logger.info("A iniciar população de dados")
        cpv_synonyms.main()
        contrato_synonymos.main()
        procedimento_Synonymos.main()
        justificacao.main()
        artigos_synonymos.main()
        logger.info("Fim da população dados")
    except Exception as e:
        logger.error(f"Erro init_dims antes do load: {e}")
        sys.exit(1)
    #endregion

    #region Load
    try:

        logger.info("A iniciar carregamento de dados")
        db.ensure_dim_data()
        db.execute_load()
        logger.success("Fim do carregamento de dados")
    except Exception as e:
        logger.error(f"Erro: {e}")
        sys.exit(1)
    #endregion

    
    Notify_laravel.main()

if __name__ == "__main__":
    main()