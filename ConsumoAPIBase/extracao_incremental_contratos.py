import time
import random
import datetime
import pandas as pd
import requests
from alive_progress import alive_bar
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import extracao_incremental_entidades as empresa
from loguru import logger
import database_aux as db
from datetime import datetime, timedelta
import json


API_URL = "https://www.base.gov.pt/Base4/pt/resultados/"

HEADERS = {
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "X-Requested-With": "XMLHttpRequest",
    "User-Agent": "Mozilla/5.0",
}

VERSION_SEARCH = "101.0"
VERSION_DETAIL = "101.0"
PAGE_SIZE = 25
MAX_PAGES = 1


def criar_sessao():
    
    sessao = requests.Session()
    tentativa = Retry(
        total=5,
        backoff_factor=2,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["POST"],
    )
    adapter = HTTPAdapter(max_retries=tentativa)
    sessao.mount("https://", adapter)
    return sessao

#Lista de contratos
def listar_contratos(sessao: requests.Session, pagina: int) :
    
    payload = {
        "type": "search_contratos",
        "version": VERSION_SEARCH,
        "query": "",
        "sort": "-publicationDate",
        "page": pagina,
        "size": PAGE_SIZE,
    }

    try:
        resposta = sessao.post(API_URL, data=payload, headers=HEADERS)
        resposta.raise_for_status()
        #print(f"Conexão a {API_URL} com sucesso")
        return resposta.json()

    except requests.exceptions.RequestException as e:
        print(f"Erro na listagem da página {pagina}: {e}")
        return None

#Vai buscar os detalhes de cada contrato
def extrair_detalhes(sessao: requests.Session, contrato_id: str):
    payload = {
        "type": "detail_contratos",
        "version": VERSION_DETAIL,
        "id": contrato_id,
    }

    try:
        resposta = sessao.post(API_URL, data=payload, headers=HEADERS, timeout=20)
        resposta.raise_for_status()
        data = resposta.json()

        if isinstance(data, dict) and "item" in data:
            return data["item"]
        return data

    except requests.exceptions.RequestException as e:
        print(f"Erro ao extrair detalhe do contrato {contrato_id}: {e}")
        return {}


#Extrair entidades
def flatten_entidade(lista: list, prefixo: str, contrato_data: dict):
    if isinstance(lista, list) and lista:
        entidade = lista[0]
        contrato_data[f"{prefixo}Nif"] = entidade.get("nif")
        contrato_data[f"{prefixo}Description"] = entidade.get("description")
        contrato_data[f"{prefixo}Id"] = entidade.get("id")
        empresa.main(entidade.get("id"))
    else:
        contrato_data[f"{prefixo}Nif"] = None
        contrato_data[f"{prefixo}Description"] = None
        contrato_data[f"{prefixo}Id"] = None

#Extrair os links 
def extrair_links_documentos(detalhes: dict) -> str:

    if detalhes is not None:
        documentos = detalhes.get("documentos") or detalhes.get("documents") or []

        if not isinstance(documentos, list) or not documentos:
            return ""

        links = [
            f"https://www.base.gov.pt/Base4/pt/resultados/?type=doc_documentos&id={doc['id']}&ext=.pdf"
            for doc in documentos
            if isinstance(doc, dict) and "id" in doc
        ]

        return " | ".join(links)
    else:
        return None

#guardar os dados do contrato
def processar_contrato(sessao: requests.Session, contrato: dict):
    contrato_data = contrato.copy()
    contrato_id = contrato["id"]

    detalhes = extrair_detalhes(sessao, contrato_id)
    if isinstance(detalhes, dict):
        contrato_data.update(detalhes)

    #Caso não seja possivel extrair dados
    if detalhes is not None:
        flatten_entidade(detalhes.get("contracting"), "contracting", contrato_data)
        flatten_entidade(detalhes.get("contracted"), "contracted", contrato_data)
        flatten_entidade(detalhes.get("contestants"), "contestants", contrato_data)


    #contrato_data.pop("contracting", None)
    #contrato_data.pop("contracted", None)

    contrato_data["links_documentos"] = extrair_links_documentos(detalhes)

    return contrato_data

def prepare_data(contrato:dict):
    contrato_data = {
        'id_contrato': contrato.get('id'),
        'tipo_contrato': contrato.get('contractTypes'),
        'tipo_procedimento': contrato.get('contractingProcedureType'),
        'objeto': contrato.get('objectBriefDescription'),
        'descricao': contrato.get('description'),
        'adjudicante': json.dumps(contrato.get('contracting')) if contrato.get('contracting') else contrato.get('contractingDescription'),
        'data_publicacao': contrato.get('publicationDate'),
        'data_celebracao': contrato.get('signingDate'),
        'valor_contratual': contrato.get('initialContractualPrice'),
        'cpvs': contrato.get('cpvs'),
        'cpvsDesignation': contrato.get('cpvsDesignation'),
        'prazo_execucao': contrato.get('executionDeadline'),
        'local_execucao': contrato.get('executionPlace'),
        'fundamentacao': contrato.get('contractFundamentationType'),
        'procedimento_centralizado': contrato.get('centralizedProcedure'),
        'num_acordos_quadro': contrato.get('frameworkAgreementProcedureId'),
        'desc_acordo_quadro': contrato.get('frameworkAgreementProcedureDescription'),
        'data_fecho_contrato': contrato.get('closeDate'),
        'valor_total_efetivo': contrato.get('totalEffectivePrice'),
        'regime': contrato.get('regime'),
        'justificacao_nao_escrita': contrato.get('nonWrittenContractJustificationTypes'),
        'tipo_fim_contrato': contrato.get('endOfContractType'),
        'crit_materiais': contrato.get('materialCriteria'),
        'concorrentes': json.dumps(contrato.get('contestants')) if contrato.get('contestants') else None,
        'adjudicatarios': json.dumps(contrato.get('contracted')) if contrato.get('contracted') else None,
        'link_pecas': contrato.get('contractingProcedureUrl'),
        'observacoes': contrato.get('observations'),
        'contrato_ecologico': contrato.get('ambientCriteria'),
        'fundamentacao_ajuste_directo': contrato.get('directAwardFundamentationType'),
    }
    return contrato_data


def main():
    sessao = criar_sessao()
    contratos = []
    pagina = 0
    parar = False
    #date of today
    today = datetime.today()

    try:
        data = listar_contratos(sessao, pagina)
        logger.info("A iniciar extração de contratos...")
        while pagina < data['total'] and not parar:
            data = listar_contratos(sessao, pagina)
            

            if not data or "items" not in data:
                #TODO:ver isto
                print("Fim dos contratos ou erro na resposta.")
                break

            items = data["items"]

            with alive_bar(len(items), title=f"Página {pagina+1}") as bar:
                for contrato in items:

                    publication_date = datetime.strptime(contrato['publicationDate'], '%d-%m-%Y')
                    #- timedelta(days=1)
                    if publication_date.date() == today.date():
                        if items is not None:
                            contrato_data = processar_contrato(sessao, contrato)
                            contrato_data = prepare_data(contrato_data)
                            contratos.append(contrato_data)
                            bar()
                    else:
                        logger.success("Dados extraidos com sucesso")
                        parar=True
                        break
            pagina += 1

            #insert data
            try:
                db.insert_data_table('contratos_ext',contratos)
                contratos.clear()
                logger.success("dados inseridos com sucesso")
            except:
                logger.error("ocorreu um erro a extrair os dados")


    except Exception as e:
        logger.exception(f"Não foi possível extrair os dados: {e}")
    logger.info("Extração finalizada com sucesso")

if __name__ == "__main__":
    main()