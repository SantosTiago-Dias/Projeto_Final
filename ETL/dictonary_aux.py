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

        # tenta UTF-8
        try:
            with open(Dictionary_file, 'r', encoding='utf-8') as f:
                return json.load(f)

        # fallback latin1/cp1252
        except UnicodeDecodeError:
            try:
                with open(Dictionary_file, 'r', encoding='latin-1') as f:
                    return json.load(f)

            except Exception:
                with open(Dictionary_file, 'w', encoding='utf-8') as f:
                    json.dump({}, f)
                return {}

        # json inválido/corrompido
        except json.JSONDecodeError:
            with open(Dictionary_file, 'w', encoding='utf-8') as f:
                json.dump({}, f)
            return {}

    return {}

def verify_id_exists(Dictionary_file:str,id:int):
    data = load_file(Dictionary_file)
    if str(id) in data:
        return True
    else:
        return False
    
def add_value(Dictionary_file:str,key:str,value:str):
    current_data=load_file(Dictionary_file)
    current_data[key]=value
    save_file(Dictionary_file, current_data)

def save_file(Dictionary_file: str, data: dict):

    with open(Dictionary_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)