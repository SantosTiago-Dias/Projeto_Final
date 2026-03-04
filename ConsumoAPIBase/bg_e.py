import time
import requests
import pandas as pd

BASE_URL = "https://www.base.gov.pt/Base4/pt/resultados/"

HEADERS = {
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "X-Requested-With": "XMLHttpRequest",
    "User-Agent": "Mozilla/5.0"
}

VERSION_SEARCH = "145.0"
VERSION_DETAIL = "116.0"

entidades = []
pagina = 0
tamanho = 25
MAX_PAG = 1 # Limitar para não overload  


# Paginação de entidades
def listar_entidades(pagina):

    payload = {
        "type": "search_entidades",
        "version": VERSION_SEARCH,
        "query": "",
        "sort": "+description",
        "page": pagina,
        "size": tamanho
    }

    resposta = requests.post(BASE_URL, data=payload, headers=HEADERS)

    if resposta.status_code == 200:
        return resposta.json()
    else:
        print("Erro na listagem:", resposta.status_code)
        return None

# Detalhes de cada entidade
def extrair_detalhes(entidade_id):

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

# Iterar páginas e entidades
while pagina < MAX_PAG:
    print(f"\nA extrair página {pagina}...")
    data = listar_entidades(pagina)
    if not data or "items" not in data:
        print("Fim das entidades.")
        break

    for entidade in data["items"]:
        entidade_data = entidade.copy()
        detalhes = extrair_detalhes(entidade["id"])

        if isinstance(detalhes, dict):
            entidade_data.update(detalhes)

        entidade_data["link_contratos"] = (
            f"https://www.base.gov.pt/Base4/pt/pesquisa/?type=contratos&adjudicatariaid={entidade['id']}"
        )

        entidades.append(entidade_data)
        print(f"Extração {entidade['id']} concluída")
        time.sleep(1)  

    pagina += 1
    time.sleep(2)


# Guardar resultados
df = pd.DataFrame(entidades)
df.to_csv("entidades.csv", sep=";", encoding="utf-8-sig")
print("CSV entidades  criado ")