from dotenv import load_dotenv
import os
import cpv_synonyms
import extracao_incremental_contratos 
import ConsumoAPIBase.extracao_completa as extracao_completa 
import pandas as pd

load_dotenv('.env')

def main():

    extracao_incremental=False      
    #Verificar se os dados existem na base de dados

    if extracao_incremental is True:
        try:
            extracao_incremental_contratos.main()
        except:
            print("ERROR na extração de contratos")
        
        try:
            cpv_synonyms.main()
        except:
            print("ERROR:cpv_synonyms")
    else:
        extracao_completa.main()

if __name__ == "__main__":
    main()