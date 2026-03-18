import pandas as pd
import json
import os
from groq import Groq
import dictonary_aux as aux
from dotenv import load_dotenv
from loguru import logger

load_dotenv('.env')

CACHE_FILE = 'dictonary_CPVs.json'
client = Groq(api_key=os.getenv('API_KEY'))

def main(CPV:str,CPV_designation:str):
    aux.verifiy_File_exists(CACHE_FILE)

    dict_data=aux.load_file(CACHE_FILE)
    if CPV in dict_data:
        return
    
    prompt = f"Gere 5 sinónimos ou termos de pesquisa para: '{CPV_designation}'. Responda apenas os termos separados por vírgula."
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}]
        )
        synonyms = response.choices[0].message.content.strip()
        dict_data[CPV]=synonyms
        #TODO:guardar na BD
        aux.save_file(CACHE_FILE, dict_data)
        
    except Exception as e:
        logger.error(f"Error: {e}")
