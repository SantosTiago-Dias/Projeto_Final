import pandas as pd
import os
import glob
from loguru import logger
import dictonary_aux as aux
from alive_progress import alive_bar
import database_aux as db
import numpy as np
import cpv_synonyms as cpv_finder

FOLDER_PATH   = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Ficheiros_extracao")

####################################################################################################
# Ficheiro responsavel por fazer a estração completa dos dados para a database
####################################################################################################
def parse_cpv(raw: str) -> dict | None:
    if not raw or not isinstance(raw, str) or ' - ' not in raw:
        return None
    
    parts = raw.split(' - ', 1)
    
    return {
        'codigo':    parts[0].strip(),
        'descricao': parts[1].strip(),
    }


def main():
    if not os.path.isdir(FOLDER_PATH):
       logger.error(f"Não existe a pasta neste caminho:{FOLDER_PATH}")
    
    xlsx_files = glob.glob(os.path.join(FOLDER_PATH, "*.xlsx"))

    for f in xlsx_files:
        name_file=os.path.basename(f)
        data= pd.read_excel(f)
        data.replace({np.nan: None})
        
        if "contratos" in name_file:
            logger.info("A iniciar extração de contactos")
            #try:
            
            db_data = []
            #para aceder a cada linha dentro do ficheiro
            with alive_bar(len(data)) as bar:
                for row in data.itertuples(index=False):
                    cpv=parse_cpv(str(row.CPV))
                    #Preparação dos dados para serem carregados para a base de dados
                    row_db = {
                        'id_contrato':                  db.sanitize(row.idcontrato),
                        'tipo_contrato':                db.sanitize(row.tipoContrato),
                        'tipo_procedimento':            db.sanitize(row.tipoprocedimento),
                        'objeto':                       db.sanitize(row.objectoContrato),
                        'descricao':                    db.sanitize(row.descContrato),
                        'adjudicante_id':               db.sanitize(row.adjudicante),
                        'data_publicacao':              db.sanitize(row.dataPublicacao),
                        'data_celebracao':              db.sanitize(row.dataCelebracaoContrato),
                        'valor_contratual':             db.sanitize(row.precoContratual),
                        'cpv':                          db.sanitize(cpv['codigo']),
                        'cpv_description':              db.sanitize(cpv['descricao']),
                        'prazo_execucao':               db.sanitize(row.prazoExecucao),
                        'local_execucao':               db.sanitize(row.LocalExecucao),
                        'fundamentacao':                db.sanitize(row.fundamentacao),
                        'procedimento_centralizado':    db.sanitize(row.ProcedimentoCentralizado),
                        'num_acordos_quadro':           db.sanitize(row.numAcordoQuadro),
                        'desc_acordo_quadro':           db.sanitize(row.DescrAcordoQuadro),
                        'data_fecho_contrato':          db.sanitize(row.dataFechoContrato),
                        'valor_total_efetivo':          db.sanitize(row.PrecoTotalEfetivo),
                        'regime':                       db.sanitize(row.regime),
                        'justificacao_nao_escrita':     db.sanitize(row.justifNReducEscrContrato),
                        'tipo_fim_contrato':            db.sanitize(row.tipoFimContrato),
                        'crit_materiais':               db.sanitize(row.CritMateriais),
                        'link_pecas':                   db.sanitize(row.linkPecasProc),
                        'observacoes':                  db.sanitize(row.Observacoes),
                        'contrato_ecologico':           db.sanitize(row.ContratEcologico),
                        'fundamentacao_ajuste_directo': db.sanitize(row.fundamentAjusteDireto),
                    }
                
                    #CPV
                    cpv_finder.main(cpv['codigo'],cpv['descricao'])

                    #Adicionar os dados ao array
                    db_data.append(row_db)

            db.insert_data_table("contratos_ext",db_data)

            #except:
                #logger.error("Aconteceu um erro a tentar extrair os contactos")

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

                    #Preparação dos dados para serem carregados para a base de dados
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