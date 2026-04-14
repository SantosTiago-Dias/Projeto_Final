import os
from cerebras.cloud.sdk import Cerebras, RateLimitError
from dotenv import load_dotenv
import dictonary_aux as dictionary
from loguru import logger
import database_aux as db
import time

load_dotenv(".env")
CCP_FILE = "Tipo_Procedimento.json"
TABLE_NAME = "tipo_procedimento_dictionary"
TABLE_LOGS = 't_logs_extract'
client = Cerebras(api_key=os.getenv('API_KEY'))

def prepare_data(artigo:int,explain:str):
    data={
        'tipo':artigo,
        'descricao':explain,
    }
    return data

def main():
    dictionary.verifiy_File_exists(CCP_FILE)
    procedureType_list_distinc=db.get_distinct_data('tipo_procedimento','contratos_ext')
    
    logger.info("A inicar a população de dados dos Tipos de procedimento")
    log_id = db.change_status(None, TABLE_LOGS, TABLE_NAME, "INICIO")

    for proceduteType in procedureType_list_distinc:
        if not dictionary.verify_id_exists(CCP_FILE,proceduteType):
            retries = 0
            while retries < 5:
                try:
                    prompt = f"""Você é um sistema de classificação de compras públicas europeias.

                    Tipo de procidimento: {proceduteType}

                    Retorna EXATAMENTE UMA FRASE onde expliques esse arigo em liguagem corrente.

                    REGRAS ESTRITAS:
                    - Responda APENAS com a frase
                    - SEM explicações, SEM introduções, SEM numeração
                    - SEM quebras de linha, SEM pontuação extra
                    - SEM observações
                    - SEM mudança de linha

                    FORMATO:
                    {proceduteType}: explicação simples.
                    """

                    response = client.chat.completions.create(
                        model="llama3.1-8b",
                        messages=[{"role": "user", "content": prompt}],
                        max_completion_tokens=100,
                    )
                    
                    explain = response.choices[0].message.content.strip()

                    dictionary.add_value(CCP_FILE,str(proceduteType),explain)
                    db.insert_data_table(TABLE_NAME,[prepare_data(proceduteType,explain)])
                    
                    time.sleep(0.3)  # polite delay between requests
                    break
    
                except RateLimitError:
                    wait = 30 * (2 ** retries)
                    logger.warning(f"Rate limit hit for '{proceduteType}'. Waiting {wait}s...")
                    time.sleep(wait)
                    retries += 1
    
                except Exception as e:
                    logger.error(f"ERROR: {e}")
                    db.change_status(log_id,TABLE_LOGS, None, "ERRO", mensagem=str(e))
                    break
    logger.info("Fim de população dos tipos de procedimentos")
    db.change_status(log_id,TABLE_LOGS, None, "SUCESSO")

if __name__ == "__main__":
    main()