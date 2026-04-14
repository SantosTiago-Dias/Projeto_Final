import os
from cerebras.cloud.sdk import Cerebras, RateLimitError
from dotenv import load_dotenv
import dictonary_aux as dictionary
from loguru import logger
import database_aux as db
import time

load_dotenv(".env")
DICTIONARY_FILE = "Justificacao_Nao_Escrita.json"
TABLE_NAME = "justificacao_contrato_nao_escrito_dictionary"
TABLE_LOGS = 't_logs_extract'

client = Cerebras(api_key=os.getenv('API_KEY'))

def prepare_data(artigo:int,explain:str):
    data={
        'justificacao':artigo,
        'descricao':explain,
    }
    return data

def main():
    dictionary.verifiy_File_exists(DICTIONARY_FILE)
    justis_list_distinc=db.get_distinct_data('justificacao_nao_escrita','contratos_ext')
    
    logger.info("A inicar a população dos Tipos de contrato")
    log_id = db.change_status(None, TABLE_LOGS, TABLE_NAME, "INICIO")

    for justi in justis_list_distinc:

        #in case the justification is null
        if not justi or not justi.strip():
            logger.warning("Justificação vazia ignorada.")
            continue

        if not dictionary.verify_id_exists(DICTIONARY_FILE,justi):
            retries = 0
            while retries < 5:
                try:
                    prompt = f"""Você é um sistema de classificação de compras públicas europeias.

                    Justificação não escrita: {justi}

                    Retorna EXATAMENTE UMA FRASE onde expliques esse arigo em liguagem corrente.

                    REGRAS ESTRITAS:
                    - Responda APENAS com a frase
                    - SEM explicações, SEM introduções, SEM numeração
                    - SEM quebras de linha, SEM pontuação extra
                    - SEM observações
                    - SEM mudança de linha

                    FORMATO:
                    {justi}: explicação simples.
                    """

                    response = client.chat.completions.create(
                        model="llama3.1-8b",
                        messages=[{"role": "user", "content": prompt}],
                        max_completion_tokens=100,
                    )
                    
                    explain = response.choices[0].message.content.strip()

                    dictionary.add_value(DICTIONARY_FILE,str(justi),explain)
                    db.insert_data_table(TABLE_NAME,[prepare_data(justi,explain)])
                    
                    time.sleep(0.3)  # polite delay between requests
                    break
    
                except RateLimitError:
                    wait = 30 * (2 ** retries)
                    logger.warning(f"Rate limit hit for '{justi}'. Waiting {wait}s...")
                    time.sleep(wait)
                    retries += 1
    
                except Exception as e:
                    logger.error(f"ERROR: {e}")
                    db.change_status(log_id,TABLE_LOGS, None, "ERRO", mensagem=str(e))
                    break

    logger.info("Fim de população dos tipo de contratos")
    db.change_status(log_id,TABLE_LOGS, None, "SUCESSO")

if __name__ == "__main__":
    main()