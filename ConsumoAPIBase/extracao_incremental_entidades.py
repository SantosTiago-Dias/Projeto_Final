import time
import requests
import pandas as pd
import os
import json
from loguru import logger
import dictonary_aux as d

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
        return {"id": entidade_id}


def main(EntityID:int):
    
    d.verifiy_File_exists(DICTIONARY_FILE)
    logger.info(f"A extrair entidade {EntityID}")
    #Procuro a entidade no dicionario se ja tiver
    if d.verify_id_exists(DICTIONARY_FILE,EntityID) is False:
        try:
            detalhes = extrair_detalhes(EntityID)

            d.save_file(DICTIONARY_FILE, data={str(EntityID): detalhes['description']})

            detalhes["link_contratos"] = (f"https://www.base.gov.pt/Base4/pt/pesquisa/?type=contratos&adjudicatariaid={EntityID}")

            print(detalhes)
        except Exception as e:
            logger.exception(f"Não foi possivel encontrar a identidade{EntityID},{e}\n")

if __name__ == "__main__":
    main(EntityID=1)