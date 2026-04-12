import os
from cerebras.cloud.sdk import Cerebras, RateLimitError
from dotenv import load_dotenv
import dictonary_aux as dictionary
from loguru import logger
import database_aux as db
import time

load_dotenv(".env")
TABLE_NAME = "tipo_contrato_dictionary"
CCP_FILE = "Tipo_Contrato.json"

client = Cerebras(api_key=os.getenv('API_KEY'))



def prepare_data(artigo:int,explain:str):
    data={
        'tipo':artigo,
        'descricao':explain,
    }
    return data

def main():
    dictionary.verifiy_File_exists(CCP_FILE)
    contractType_list_distinc=db.get_distinct_data('tipo_contrato','contratos_transf')
    
    log_id = db.change_status_extraction(None, TABLE_NAME, "INICIO")
    logger.info("A inicar a população dos Tipos de contrato")

    for contractType in contractType_list_distinc:
        if not dictionary.verify_id_exists(CCP_FILE,contractType):
            retries = 0
            while retries < 5:
                try:
                    prompt = f"""Você é um sistema de classificação de compras públicas europeias.

                    Tipo de contrato: {contractType}

                    Retorna EXATAMENTE UMA FRASE onde expliques esse arigo em liguagem corrente.

                    REGRAS ESTRITAS:
                    - Responda APENAS com a frase
                    - SEM explicações, SEM introduções, SEM numeração
                    - SEM quebras de linha, SEM pontuação extra
                    - SEM observações
                    - SEM mudança de linha

                    FORMATO:
                    {contractType}: explicação simples.
                    """

                    response = client.chat.completions.create(
                        model="llama3.1-8b",
                        messages=[{"role": "user", "content": prompt}],
                        max_completion_tokens=100,
                    )
                    
                    explain = response.choices[0].message.content.strip()

                    dictionary.add_value(CCP_FILE,str(contractType),explain)
                    db.insert_data_table(TABLE_NAME,[prepare_data(contractType,explain)])
                    
                    time.sleep(0.3)  # polite delay between requests
                    break
    
                except RateLimitError:
                    wait = 30 * (2 ** retries)
                    logger.warning(f"Rate limit hit for '{contractType}'. Waiting {wait}s...")
                    db.change_status_extraction(log_id, None, "ERRO", mensagem=str(e))
                    time.sleep(wait)
                    retries += 1
    
                except Exception as e:
                    logger.error(f"ERROR: {e}")
                    break
    logger.info("Fim de população dos tipo de contratos")
    db.change_status_extraction(log_id, None, "SUCESSO")

if __name__ == "__main__":
    main()