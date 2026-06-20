from loguru import logger
import database_aux as db
import extracao_incremental_entidades as extracao_entidades

TABLE_NAME = "entidades_ext"
TABLE_LOGS= "t_logs_extract"

#Function to retry the extraction of entities that were not found in the dimension table
#when they are bigger then 5
def main():

    #List of entities that were not found in dim
    list_entity_not_found = db.getEntitynotFound()

    #if the list is empty
    if not list_entity_not_found:
        logger.info("Não existem entidades por atualizar.")
        return

    if len(list_entity_not_found) >= 5:
        for entity_id in list_entity_not_found:
            log_id = db.change_status(None, TABLE_LOGS,TABLE_NAME, "INICIO","Retry Entity:{entity_id}")
            logger.info(f"A tentar novamente extrair dados da entidade: {entity_id}")
            detalhes = extracao_entidades.extrair_detalhes(entity_id)
            if detalhes:
                db.insert_data_table(TABLE_NAME, [extracao_entidades.prepare_data(detalhes)])
                db.change_status(log_id,TABLE_LOGS, None, "SUCESSO", f"Entidade {entity_id} atualizada com sucesso.")
                logger.info(f"Entidade {entity_id} atualizada com sucesso.")
            else:
                db.change_status(log_id,TABLE_LOGS, None, "ERRO", f"Falha ao tentar extrair novamente dados da entidade {entity_id}.")
                logger.error(f"Falha ao extrair dados da entidade {entity_id}")
            
