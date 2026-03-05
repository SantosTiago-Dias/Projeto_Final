import pandas as pd
import json
import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv('.env')

CACHE_FILE = 'dictonary_CPVs.json'
CONTRATOS_FILE = '../contratos.csv'
client = Groq(api_key=os.getenv('API_KEY'))

def main():
    # 1. Verificação se o dicionario ja existe caso não exista ainda criamos para guardar dados JSON la dentro
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, 'r', encoding='utf-8') as f:
            try:
                cpv_cache = json.load(f)
            except json.JSONDecodeError:
                cpv_cache = {}
    else:
        cpv_cache = {}
        with open(CACHE_FILE, 'w', encoding='utf-8') as f:
            json.dump(cpv_cache, f)

    #Carregamento dos dados de contratos
    df = pd.read_csv(CONTRATOS_FILE, sep=';')

    def get_synonyms_smart(cpv_code, designation):
        if str(cpv_code) in cpv_cache:
            return cpv_cache[str(cpv_code)]

        print(f"New CPV detected: {cpv_code} ({designation}). Generating synonyms...")
        prompt = f"Gere 5 sinónimos ou termos de pesquisa para: '{designation}'. Responda apenas os termos separados por vírgula."

        try:
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}]
            )
            synonyms = response.choices[0].message.content.strip()
            cpv_cache[str(cpv_code)] = synonyms
            #TODO:GUADAR ESTES DADOS TANTO NA TABELA DE BASE DE DADOS
            #COMO NO DICIONARIO

            return synonyms
        except Exception as e:
            print(f"Error: {e}")
            synonyms = "termo geral"

    #Eliminar os dados duplicados
    unique_items = df[['cpvs', 'cpvsDesignation']].drop_duplicates()

    #Percorrer cada uma para ir buscar os seus "sinonimos"
    for _, row in unique_items.iterrows():
        get_synonyms_smart(row['cpvs'], row['cpvsDesignation'])

    # 4. Salva os sinonimos no dicionario
    print(cpv_cache)
    with open(CACHE_FILE, 'w', encoding='utf-8') as f:
        json.dump(cpv_cache, f, ensure_ascii=False, indent=4)

    print("Procura de sinonimos completa")