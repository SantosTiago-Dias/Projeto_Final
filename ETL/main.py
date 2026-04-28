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

    
    #region Connecção com a BD
    connection = db.get_connection()
    if not connection:
        logger.error("Não foi possivel estabelecer uma connecção com a base de dados")
        sys.exit(1)
    #endregion    

    #region Extração
    try:
        db.verify_database_exists()
        extracao_incremental_contratos.main()    
    except Exception as e:
        logger.error(f"Erro: {e}")
        sys.exit(1)
    #endregion

    #region Transformação
    try:
        logger.info("A iniciar transformação de dados")
        db.execute_transformacao()
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
        db.execute_load()
        db.ensure_dim_data()
        logger.success("Fim do carregamento de dados")
    except Exception as e:
        logger.error(f"Erro: {e}")
        sys.exit(1)
    #endregion


if __name__ == "__main__":
    main()