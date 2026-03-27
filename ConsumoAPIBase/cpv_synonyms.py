import pandas as pd
import json
import os
from cerebras.cloud.sdk import Cerebras, RateLimitError
from dotenv import load_dotenv
import dictonary_aux as aux
from loguru import logger
import database_aux as db
import time

load_dotenv('.env')

CACHE_FILE = 'dictonary_CPVs.json'
client = Cerebras(api_key=os.getenv('API_KEY'))
 
def main(cpv_list: list):
 
    aux.verifiy_File_exists(CACHE_FILE)
    dictionary_data = aux.load_file(CACHE_FILE)
 
    cpv_list = list(set(cpv_list))
 
    synonyms_dict = {}
 
    for cpv in cpv_list:
        prompt = f"Gere 5 sinónimos ou termos de pesquisa em portugues portugal para: '{cpv}'. Responda apenas os termos separados por vírgula."
 
        retries = 0
        while retries < 5:
            try:
                response = client.chat.completions.create(
                    model="llama3.1-8b",
                    messages=[{"role": "user", "content": prompt}],
                    max_completion_tokens=100,
                )
                logger.info("request")
                synonyms = response.choices[0].message.content.strip()
                synonyms_dict[cpv] = synonyms
                time.sleep(0.3)  # polite delay between requests
                break
 
            except RateLimitError:
                wait = 30 * (2 ** retries)  # 30s, 60s, 120s...
                logger.warning(f"Rate limit hit for '{cpv}'. Waiting {wait}s...")
                time.sleep(wait)
                retries += 1
 
            except Exception as e:
                logger.error(f"ERROR: {e}")
                synonyms_dict[cpv] = "termo geral"
                break
 
    aux.save_file(CACHE_FILE, dictionary_data)