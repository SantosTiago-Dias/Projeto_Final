import pandas as pd
import os
import glob
from loguru import logger
import dictonary_aux as aux
from alive_progress import alive_bar
import database_aux as db
import numpy as np

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
        data.replace({np.nan: None})
        
        #if "contratos" in name_file:
        #TODO:AO extrair os contratos verificar se os msm tem adjudicatarios caso n tenham ir buscar os dados do contrato a API
        # e por o valor cocontratantes
        #    print("contratos")
        #    print(data)

        if "entidade" in name_file:

            logger.info("Extrair entidades") 
            FILENAME = 'dictonary_Entity.json'
            aux.verifiy_File_exists(FILENAME)
            dictionary_data  = aux.load_file(FILENAME)
            db_data = []
            #para aceder a cada linha dentro do ficheiro
            with alive_bar(len(data)) as bar:
                for row in data.itertuples(index=False):
                    nif = str(row.nifEntidade)

                    #Escolhe os dados que vão ser guardados
                    row_db  = {
                        'nif':                         db.sanitize(str(row.nifEntidade)),
                        'nome':                        db.sanitize(row.desigEntidade),
                        'total_adjudicatario':         db.sanitize(row.totAdjudicatario),
                        'num_contratos_adjudicatario': db.sanitize(row.numContratos),
                        'total_adjudicante':           db.sanitize(row.totAdjudicante),
                        'num_contratos_adjudicante':   db.sanitize(row.totAdjudicanteValorContratIni),
                        'pais':                        db.sanitize(row.descPais),
                    }

                    db_data.append(row_db)
                    if nif not in dictionary_data  and nif != '-':
                        dictionary_data [nif] = row.desigEntidade
                    bar()

            aux.save_file(FILENAME, dictionary_data)
            
            db.insert_data_table("entidade_ext",db_data)

if __name__ == "__main__":
    main()