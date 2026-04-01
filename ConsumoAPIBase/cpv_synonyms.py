import os
from cerebras.cloud.sdk import Cerebras, RateLimitError
from dotenv import load_dotenv
import dictonary_aux as dictonary
from loguru import logger
import database_aux as db
import time

load_dotenv('.env')

CACHE_FILE = 'dictonary_CPVs.json'
client = Cerebras(api_key=os.getenv('API_KEY'))

def prepare_data(cpv:int,description:str):
    data={
        'codigo':cpv,
        'descricao':description,
    }
    return data
 
def main():
    dictonary.verifiy_File_exists(CACHE_FILE)
    cpv_list_distinc=db.get_distinct_data('cpvs','contratos_ext')

    logger.info("A iniciar a população de dados dos cpv")
    for cpv in cpv_list_distinc:
        prompt = f"""Você é um sistema de classificação de compras públicas europeias.

        Dado o código CPV: {cpv}

        Retorne EXATAMENTE 5 sinônimos ou termos correntes para esse código CPV.

        REGRAS ESTRITAS:
        - Responda APENAS com os 5 termos separados por vírgula
        - SEM explicações, SEM introduções, SEM numeração
        - SEM quebras de linha, SEM pontuação extra
        - SEM frases como "Os sinônimos são:" ou similares
        - SEM observações
        - SEM mudançpa de linha
        - SEM frases "Aqui estão 5 sinônimos ou termos correntes para o código CPV"

        FORMATO OBRIGATÓRIO (siga exatamente):
        termo1,termo2,termo3,termo4,termo5"""
        if not dictonary.verify_id_exists(CACHE_FILE,cpv):
            retries = 0
            while retries < 5:
                try:
                    response = client.chat.completions.create(
                        model="llama3.1-8b",
                        messages=[{"role": "user", "content": prompt}],
                        max_completion_tokens=100,
                    )
                    
                    synonyms = response.choices[0].message.content.strip()

                    dictonary.add_value(CACHE_FILE,str(cpv),synonyms)
                    db.insert_data_table('cpv_dictionary_ext',[prepare_data(cpv,synonyms)])
                    
                    time.sleep(0.3)  # polite delay between requests
                    break
    
                except RateLimitError:
                    wait = 30 * (2 ** retries)  # 30s, 60s, 120s...
                    logger.warning(f"Rate limit hit for '{cpv}'. Waiting {wait}s...")
                    time.sleep(wait)
                    retries += 1
    
                except Exception as e:
                    logger.error(f"ERROR: {e}")
                    break
    logger.info("Fim de extração de cpv")

if __name__ == "__main__":
    main()



