"""
================================================================================
                            ETL PIPELINE - MAIN ORCHESTRATOR
================================================================================

PURPOSE:
    This module orchestrates the complete Extract-Transform-Load (ETL) pipeline
    for processing contract data into a dimensional data warehouse.

FLOW OVERVIEW:
    1. CONNECTION → Establish database connection
    2. EXTRACTION → Verify database structure exists
    3. TRANSFORMATION → Apply business logic transformations
    4. POPULATION → Load reference data and synonyms
    5. LOAD → Populate fact and dimension tables

EXECUTION SEQUENCE:
    ┌─────────────────────┐
    │  DATABASE CONNECT   │ - Establish connection to warehouse
    │                     │ - Exit if connection fails
    └──────────┬──────────┘
               ↓
    ┌─────────────────────┐
    │   VERIFY DATABASE   │ - Check schema exists
    │                     │ - Prepare for transformation
    └──────────┬──────────┘
               ↓
    ┌─────────────────────┐
    │  TRANSFORMATION     │ - Execute transformacao()
    │                     │ - Create/update dimensions
    │                     │ - Build star schema
    └──────────┬──────────┘
               ↓
    ┌─────────────────────┐
    │   DATA POPULATION   │ - Load CPV synonyms
    │   (5 modules):      │ - Load contract types
    │                     │ - Load procedure types
    │   • cpv_synonyms    │ - Load justifications
    │   • tipoContratos   │ - Load articles
    │   • tipoProcedim    │
    │   • justificacao    │
    │   • artigos         │
    └──────────┬──────────┘
               ↓
    ┌─────────────────────┐
    │    FINAL LOAD       │ - Ensure date dimension
    │                     │ - Load fact table
    │                     │ - Complete warehouse
    └─────────────────────┘

ERROR HANDLING:
    - Each phase is wrapped in try-catch
    - Errors logged with loguru
    - Process exits immediately on failure (sys.exit(1))
    - No partial data loads

DEPENDENCIES:
    - database_aux: Core database operations
    - cpv_synonyms: CPV classification loading
    - tipoContratos_synonymos: Contract type loading
    - tipoProcedimento_synonymos: Procedure type loading
    - justificacaoNEscrita: Justification data loading
    - artigos_synonymos: Article/regulation loading
    - dictonary_aux: Helper utilities

For detailed documentation, see: FLOW_DOCUMENTATION.md
================================================================================
"""

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
        #extracao_incremental_contratos.main()
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
        db.ensure_dim_data()
        db.execute_load()
        logger.success("Fim do carregamento de dados")
    except Exception as e:
        logger.error(f"Erro: {e}")
        sys.exit(1)
    #endregion


if __name__ == "__main__":
    main()