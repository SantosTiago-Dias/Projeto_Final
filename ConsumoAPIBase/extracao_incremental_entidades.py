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

HEADERS = {
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "X-Requested-With": "XMLHttpRequest",
    "User-Agent": "Mozilla/5.0"
}
VERSION_SEARCH = "145.0"
VERSION_DETAIL = "116.0"
   

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
        return None  # retorna None em vez de dicionário parcial


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
    logger.info(f"A extrair entidade {EntityID}")
    #Procuro a entidade no dicionario se ja tiver
    if not dictonary.verify_id_exists(DICTIONARY_FILE,EntityID):
        try:
            detalhes = extrair_detalhes(EntityID)

            #Garante que não há crash se detalhes for None
            if not detalhes or not isinstance(detalhes, dict):
                logger.warning(f"Entidade {EntityID} não encontrada ou inválida")
            else:
                descricao = detalhes.get('description')
                dictonary.add_value(DICTIONARY_FILE, str(EntityID), descricao)

                db.insert_data_table("entidades_ext", [prepare_data(detalhes)])

        except Exception as e:
            logger.exception(f"Não foi possivel encontrar a entidade {EntityID}: {e}\n")

if __name__ == "__main__":
    main(EntityID=1)