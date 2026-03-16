import os
import json
####################################################################
#Ficheiro repsonsavel por gerar o dicionario de dados
########################################################################

def verifiy_File_exists(Dictionary_file:str):
    if not os.path.exists(Dictionary_file):
        with open(Dictionary_file, 'w', encoding='utf-8') as file:
            json.dump({}, file)

def load_file(Dictionary_file: str):
    """Load the entire JSON file into memory once."""
    if os.path.exists(Dictionary_file):
        try:
            with open(Dictionary_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError:
            # File is corrupted, start fresh
            with open(Dictionary_file, 'w', encoding='utf-8') as f:
                json.dump({}, f)
            return {}
    return {}

def verify_id_exists(Dictionary_file:str,id:int):
    if str(id) not in Dictionary_file:
        return False
    else:
        return True

def save_file(Dictionary_file: str, data: dict):
   with open(Dictionary_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)