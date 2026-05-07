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
TABLE_NAME = "contratos_ext"
HEADERS = {
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "X-Requested-With": "XMLHttpRequest",
    "User-Agent": "Mozilla/5.0",
}
TABLE_LOGS= "t_logs_extract"
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
def listar_contratos(sessao: requests.Session, pagina: int, retries: int = 5):
    
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
        data = resposta.json()
        
        # Validate the response has actual content
        if not data or "items" not in data or "total" not in data:
            raise ValueError(f"Resposta inválida da API: {data}")
        
        return data

    except (requests.exceptions.RequestException, ValueError) as e:
        logger.error(f"Erro na listagem da página {pagina}: {e}")
        if retries > 0:
            logger.info(f"Tentativa {6 - retries} de 5")
            wait_seconds = 30 * 60  # 30 minutes
            logger.info(f"A aguardar 30 minutos antes de tentar novamente...")
            time.sleep(wait_seconds)
            return listar_contratos(sessao, pagina, retries - 1)
        else:
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
        for entidade in lista:
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

def extracion_contracts(sessao:requests.session):
    contratos = []
    pagina = 0
    parar = False
    yesterday = datetime.today() - timedelta(days=1)
    num_contratos = 0   
    
    try:
        while not parar:
            
            data = listar_contratos(sessao, pagina)

            # If data is NULL 
            if data is None:
                logger.error(f"Falha ao obter dados para a página {pagina}. A cancelar extração.")
                db.change_status(None, TABLE_LOGS, TABLE_NAME, "ERRO", mensagem="Não foi possível iniciar a extração de contratos.")
                break
            
            items = data["items"]

            with alive_bar(len(items), title=f"Página {pagina+1}") as bar:
                for contrato in items:

                    publication_date = datetime.strptime(contrato['publicationDate'], '%d-%m-%Y')

                    if publication_date.date() == yesterday.date():
                        if items is not None:
                            contrato_data = processar_contrato(sessao, contrato)
                            contrato_data = prepare_data(contrato_data)
                            contratos.append(contrato_data)
                            num_contratos += 1
                            bar()
                    elif publication_date.date() < yesterday.date():
                        logger.success("Dados extraidos com sucesso")
                        parar = True
                        break
            pagina += 1

            #insert data
            if contratos:
                log_id = db.change_status(None, TABLE_LOGS,TABLE_NAME, "INICIO")
                try:
                    
                    db.insert_data_table(TABLE_NAME,contratos)
                    contratos.clear()
                    db.change_status(log_id,TABLE_LOGS, None, "SUCESSO")
                except Exception as e:
                    logger.error("ocorreu um erro a extrair os dados")
                    db.change_status(log_id,TABLE_LOGS, None, "ERRO", mensagem=str(e))

        return num_contratos
    except Exception as e:
        logger.exception(f"Não foi possível extrair os dados: {e}")
        db.change_status(None,TABLE_LOGS, None, "ERRO", mensagem=str(e))
        

def main():
    sessao = criar_sessao()
    
    num_contratos = 0
    num_contratos = extracion_contracts(sessao)
    average_contratos = db.get_average_contracts_extracted()

    if average_contratos is not None:
        if float(num_contratos) < float(average_contratos):
            logger.info(f"Número de contratos extraídos ({num_contratos}) é inferior à média histórica ({average_contratos}). Repetindo extração.")
            num_contratos = extracion_contracts(sessao)
            
    logger.success("Extração finalizada com sucesso")
    logger.info(f"Número de contratos extraidos: {num_contratos}")
    db.average_extrated_contracts(num_contratos)

if __name__ == "__main__":
    main()