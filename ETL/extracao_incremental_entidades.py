import time
import requests
import pandas as pd
import os
import json
from loguru import logger
import dictonary_aux as dictonary
import database_aux as db

DICTIONARY_FILE = 'dictonary_Entity.json'
BASE_URL = "https://www.base.gov.pt/Base4/pt/resultados/"
TABLE_NAME = "entidades_ext"
HEADERS = {
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "X-Requested-With": "XMLHttpRequest",
    "User-Agent": "Mozilla/5.0"
}
VERSION_SEARCH = "145.0"
VERSION_DETAIL = "116.0"
TABLE_LOGS= "t_logs_extract"

# Detalhes de cada entidade
def extrair_detalhes(entidade_id:int):

    payload = {
        "type": "detail_entidades",
        "version": VERSION_DETAIL,
        "id": entidade_id
    }

    resposta = requests.post(BASE_URL, data=payload, headers=HEADERS)

    if resposta.status_code == 200:
        return resposta.json()
    else:
        print(f"Erro ao extrair detalhe {entidade_id}: {resposta.status_code}")
        return None


def prepare_data(entidade:dict):
    entidade={
        'id_entidade':entidade.get('id'),
        'nif':entidade.get('nif'),
        'nome':entidade.get('description'),
        'pais':entidade.get('location')
    }
    return entidade


def main(EntityID:int):
    
    dictonary.verifiy_File_exists(DICTIONARY_FILE)
    
    #Procuro a entidade no dicionario se ja tiver
    if not dictonary.verify_id_exists(DICTIONARY_FILE,EntityID):
        logger.info(f"A extrair entidade {EntityID}")
        log_id = db.change_status(None, TABLE_LOGS,TABLE_NAME, "INICIO")
        try:
            detalhes = extrair_detalhes(EntityID)

            if not detalhes or not isinstance(detalhes, dict):
                logger.warning(f"Entidade {EntityID} não encontrada ou inválida")
                db.change_status(log_id,TABLE_LOGS, None, "ERRO", mensagem=str(e))
            else:
                descricao = detalhes.get('description')
                dictonary.add_value(DICTIONARY_FILE, str(EntityID), descricao)
                db.insert_data_table(TABLE_NAME, [prepare_data(detalhes)])
                db.change_status(log_id,TABLE_LOGS, None, "SUCESSO")

        except Exception as e:
            logger.exception(f"Não foi possivel encontrar a entidade {EntityID}: {e}\n")
            db.change_status(log_id,TABLE_LOGS, None, "ERRO", mensagem=str(e))

if __name__ == "__main__":
    main(EntityID=1)