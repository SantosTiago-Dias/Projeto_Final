from loguru import logger
import database_aux as db
import extracao_incremental_entidades as extracao_entidades

#TODO: Adicionar loggers
#FUNCTION TO 
def main():
    list_entity_not_found = db.getEntitynotFound()
    for entity_id in list_entity_not_found:
        logger.info(entity_id)
        data=extracao_entidades.extrair_detalhes(entidade_id=entity_id)
        if data is not None:
            logger.info(data)
            updated_data = 'nome = "'+ data.get('description').upper().strip() +'", nif = "'+ data.get('nif').strip() +'", pais = "'+data.get('location').strip()+'"'
            logger.info(updated_data)
            logger.info( type(updated_data))
            db.updateEntity(updated_data, entity_id)
            logger.info(f"Dados da entidade {entity_id} atualizados")
