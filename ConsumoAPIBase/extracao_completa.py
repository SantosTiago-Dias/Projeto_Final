import pandas as pd
import os
import glob
from loguru import logger
import dictonary_aux as aux
from alive_progress import alive_bar

FOLDER_PATH   = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Ficheiros_extracao")

####################################################################################################
# Ficheiro responsavel por fazer a estração completa dos dados para a database
####################################################################################################

def main():
    if not os.path.isdir(FOLDER_PATH):
       logger.error(f"Não existe a pasta neste caminho:{FOLDER_PATH}")
    
    xlsx_files = glob.glob(os.path.join(FOLDER_PATH, "*.xlsx"))

    for f in xlsx_files:
        name_file=os.path.basename(f)
        data= pd.read_excel(f)
        
        #if "contratos" in name_file:
        #    print("contratos")
        #    print(data)

        if "entidade" in name_file:

            logger.info("Extrair entidades") 
            FILENAME = 'dictonary_Entity.json'
            aux.verifiy_File_exists(FILENAME)
            existing  = aux.load_file(FILENAME)

            #para aceder a cada linha dentro do ficheiro
            with alive_bar(len(data )) as bar:
                for row in data.itertuples(index=False):
                    nif = str(row.nifEntidade)
                    if nif not in existing  and nif != '-':
                        existing [nif] = row.desigEntidade
                    bar()

            aux.save_file(FILENAME, existing)
            logger.success("Entidades extraidas com sucesso") 

if __name__ == "__main__":
    main()