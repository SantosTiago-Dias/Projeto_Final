import os
from groq import Groq, RateLimitError
from dotenv import load_dotenv
import dictonary_aux as dictionary
from loguru import logger
import database_aux as db
import time

load_dotenv('.env')
CACHE_FILE = 'dictonary_CPVs.json'
TABLE_NAME = "cpv_dictionary"
TABLE_LOGS = 't_logs_transformacao'

client = Groq(api_key=os.getenv('GROQ_API_KEY'))

#Prepare data for insertion in the database
def prepare_data(cpv:int, cpv_description: str, description:str):
    data={
        'codigo':cpv,
        'cpv_descricao': cpv_description,
        'descricao':description
    }
    return data

#Main function to extract cpv synonyms and insert in the database
def main():
    dictionary.verifiy_File_exists(CACHE_FILE)
    cpv_list_distinc=db.get_distinct_data('cpv,cpv_descricao','cpv_contratos_transf')

    log_id = db.change_status(None, TABLE_LOGS, TABLE_NAME, "INICIO")
    logger.info("A iniciar a população de dados dos cpv")

    for cpv, cpv_descricao in cpv_list_distinc:
        prompt = f"""Você é um sistema de classificação de compras públicas europeias.

        Dado o código CPV: {cpv} - {cpv_descricao}, forneça 5 sinônimos ou termos correntes que possam ser usados para se referir a esse código CPV em um contexto de compras públicas.

        REGRAS ESTRITAS:
        - Responda APENAS com os 5 termos separados por vírgula
        - SEM explicações, SEM introduções, SEM numeração
        - SEM quebras de linha, SEM pontuação extra
        - SEM frases como "Os sinônimos são:" ou similares
        - SEM observações
        - SEM mudança de linha
        - SEM frases "Aqui estão 5 sinônimos ou termos correntes para o código CPV"
        - SEM palavras de ligação
        - TUDO EM LOWERCASE

        FORMATO OBRIGATÓRIO (siga exatamente):
        termo1,termo2,termo3,termo4,termo5"""

        if not dictionary.verify_id_exists(CACHE_FILE, cpv):
            retries = 0
            while retries < 5:
                try:
                    response = client.chat.completions.create(
                        model="llama-3.1-8b-instant",
                        messages=[{"role": "user", "content": prompt}],
                        temperature=0.2,
                    )

                    synonyms = response.choices[0].message.content.strip()

                    dictionary.add_value(CACHE_FILE,str(cpv),synonyms)
                    db.insert_data_table(TABLE_NAME,[prepare_data(cpv, cpv_descricao, synonyms)])

                    time.sleep(0.3)  # polite delay between requests
                    break
    
                except RateLimitError:
                    wait = 30 * (2 ** retries)  # 30s, 60s, 120s...
                    logger.warning(f"Rate limit hit for '{cpv}'. Waiting {wait}s...")
                    time.sleep(wait)
                    retries += 1
    
                except Exception as e:
                    logger.error(f"ERROR: {e}")
                    db.change_status(log_id, TABLE_LOGS, None, "ERRO", mensagem=str(e))
                    break

    logger.info("Fim de extração de cpv")
    db.change_status(log_id, TABLE_LOGS, None, "SUCESSO")

if __name__ == "__main__":
    main()