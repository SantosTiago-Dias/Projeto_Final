import time
import random
import requests
import pandas as pd
from requests.adapters import HTTPAdapter
from alive_progress import alive_bar
from urllib3.util.retry import Retry

API_URL = "https://www.base.gov.pt/Base4/pt/resultados/"

#TODO:PENSAR NA PARTE DE EXTRAÇÃO INCREMENTAL
#USAR DICIONARIO DE EMPRESAS SOLUÇÃO TALVEZ????
def main(extracao_incremental):
    # Configuração de sessão com retries
    sessao = requests.Session()

    tentativa = Retry(
        total=5,
        backoff_factor=2,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["POST"]
    )

    adapter = HTTPAdapter(max_retries=tentativa)
    sessao.mount("https://", adapter)

    HEADERS = {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "X-Requested-With": "XMLHttpRequest",
        "User-Agent": "Mozilla/5.0"
    }

    VERSION_SEARCH = "101.0"
    VERSION_DETAIL = "101.0"

    contratos = []
    pagina = 0
    tamanho = 25
    MAX_PAG = 1

    # Paginação de contratos
    def listar_contratos(pagina):

        payload = {
            "type": "search_contratos",
            "version": VERSION_SEARCH,
            "query": "",
            "sort": "-publicationDate",
            "page": pagina,
            "size": tamanho
        }

        try:
            resposta = sessao.post(API_URL, data=payload, headers=HEADERS)
            resposta.raise_for_status()
            print(f"Connecção ao {API_URL} com sucesso")
            return resposta.json()
        
        except requests.exceptions.RequestException as e:
            print(f"Erro listagem página {pagina}: {e}")
            return None


    # Detalhes de cada contrato
    def extrair_detalhes(contract_id):

        payload = {
            "type": "detail_contratos",
            "version": VERSION_DETAIL,
            "id": contract_id
        }

        try:
            resposta = sessao.post(
                API_URL,
                data=payload,
                headers=HEADERS,
                timeout=20
            )
            resposta.raise_for_status()
            data = resposta.json()
            if isinstance(data, dict) and "item" in data:
                return data["item"]
            return data
        
        except requests.exceptions.RequestException as e:
            print(f"Erro extrair detalhe {contract_id}: {e}")
            return {}

    # Atributos conpostos (contracting/contracted)
    def flatten_entidade(lista, prefixo, contrato_data):

        if isinstance(lista, list) and len(lista) > 0:
            entidade = lista[0]
            contrato_data[f"{prefixo}Nif"] = entidade.get("nif")
            contrato_data[f"{prefixo}Description"] = entidade.get("description")
            contrato_data[f"{prefixo}Id"] = entidade.get("id")
        else:
            contrato_data[f"{prefixo}Nif"] = None
            contrato_data[f"{prefixo}Description"] = None
            contrato_data[f"{prefixo}Id"] = None

    # Iterar páginas e contratos
    while pagina < MAX_PAG:
        with alive_bar(pagina) as bar:
            print(f"\n A iniciar extração de contratos...")
            print(f"\nA extrair página {pagina}...")

            data = listar_contratos(pagina)
            if not data or "items" not in data:
                print("Fim dos contratos.")
                break
            for contrato in data["items"]:
                #Dados "simples" do contrato
                contrato_data = contrato.copy()
                contrato_id = contrato["id"]
                
                #detalhes em si do contrato todo
                detalhes = extrair_detalhes(contrato_id)
                if isinstance(detalhes, dict):
                    contrato_data.update(detalhes)
                
                flatten_entidade(detalhes.get("contracting"), "contracting", contrato_data)
                flatten_entidade(detalhes.get("contracted"), "contracted", contrato_data)

                contrato_data.pop("contracting", None)
                contrato_data.pop("contracted", None)

                # Links de documentos
                contrato_data["links_documentos"] = ""
                documentos = (detalhes.get("documentos") or detalhes.get("documents") or [])

                if isinstance(documentos, list) and len(documentos) > 0:
                    links_docs = []
                    for doc in documentos:
                        if isinstance(doc, dict) and "id" in doc:
                            doc_id = doc["id"]
                            link_doc = (f"https://www.base.gov.pt/Base4/pt/resultados/?type=doc_documentos&id={doc_id}&ext=.pdf")
                            links_docs.append(link_doc)
                    contrato_data["links_documentos"] = " | ".join(links_docs)

                contratos.append(contrato_data)
                time.sleep(random.uniform(1.5, 3.5))

            pagina += 1
            bar()
            time.sleep(random.uniform(3, 6))

    # Guardar resultados
    df = pd.DataFrame(contratos)
    df.to_csv("contratos.csv",  sep=";", encoding="utf-8-sig")
    print("CSV contratos criado") 

if __name__ == "__main__":
    main(extracao_incremental=False)