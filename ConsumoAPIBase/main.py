from dotenv import load_dotenv
import os
import cpv_synonyms
import bg_c as contratos
import bg_e as empresa

load_dotenv('.env')

def main():

    extracao_incremental=False      
    
    #TODO:USAR a base de dados como maneira de saber se é
    #extração incremental ou extração completa

    contratos.main(extracao_incremental)
    empresa.main(extracao_incremental)
    cpv_synonyms.main()

if __name__ == "__main__":
    main()