from dotenv import load_dotenv
from loguru import logger
import mysql.connector
from mysql.connector import Error
import os
import math
import re

load_dotenv('.env')
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INIT = os.path.join(BASE_DIR, 'init.sql')
PROCEDURES = os.path.join(BASE_DIR, 'procedures.sql')

def get_connection():
    try:
        return mysql.connector.connect(
            host=os.getenv("MYSQL_HOST", "database"),
            user=os.getenv("DB_USER", "root"),
            port=int(os.getenv("MYSQL_PORT", 3306)),
            password=os.getenv("MYSQL_ROOT_PASSWORD", ""),
            database=os.getenv("MYSQL_DATABASE", "ETL")
        )
    except Error as e:
        logger.error(f"Erro ao conectar à BD: {e}")
        return False
    
def verify_database_exists():
    mydb = get_connection()
    if not mydb:
        return

    mycursor = mydb.cursor()
    try:
        mycursor.execute(f"USE {os.getenv('MYSQL_DATABASE')}")
        mycursor.execute("SHOW TABLES")
        mycursor.fetchall()

        with open(INIT, 'r', encoding='utf-8') as f:
            sql = f.read()
            for statement in sql.split(';'):
                statement = statement.strip()
                if statement:
                    mycursor.execute(statement)
        
        with open(PROCEDURES, 'r', encoding='utf-8') as f:
            sql_content = f.read()
            
            statements = sql_content.split('$$')
            for statement in statements:
                clean_stmt = statement.replace('DELIMITER', '').strip()
                if clean_stmt and clean_stmt != ';':
                    try:
                        # Ensure we handle the semicolon at the end if it was 'DELIMITER ;'
                        if clean_stmt.startswith(';'):
                            clean_stmt = clean_stmt[1:].strip()
                        
                        mycursor.execute(clean_stmt)
                    except Exception as e:
                        logger.error(f"Error executing statement: {e}")
                        mydb.rollback()
                        return False

        mydb.commit()

    except FileNotFoundError:
        logger.error("Ficheiro init.sql não encontrado")
        return False
    except mysql.connector.Error as e:
        logger.error(f"Erro ao criar tabelas: {e}")
        return False
    finally:
        mycursor.close()
        mydb.close()
   

def execute_transformacao():
    
    mydb = get_connection()
    if not mydb:
        return

    try:
        procedures = [
            "transform_detalhes_contratos",
            "transform_contratos",
            "transform_entidades",
            "transform_cpv_contratos"
        ]

        for proc in procedures:
            logger.info(f"A executar: {proc}")

            log_id = change_status(None,'t_logs_transformacao',proc,"INICIO")

            cur = mydb.cursor()
            try:
                cur.callproc(proc)

                # Drena todos os result sets
                for result in cur.stored_results():
                    try:
                        result.fetchall()
                    except Exception:
                        pass

                while cur.nextset():
                    pass

                mydb.commit()
                change_status(log_id, 't_logs_transformacao', None, "SUCESSO")
                logger.success(f"Concluído: {proc}")

            except mysql.connector.Error as e:
                logger.error(f"Erro em {proc}: {e}")
                change_status(log_id, 't_logs_transformacao', None, "ERRO", mensagem=str(e))
            

            finally:
                cur.close()

        logger.info("Transformação concluída com sucesso!")

    except mysql.connector.Error as e:
        logger.error(f"Erro na transformação: {e}")
    finally:
        mydb.close()

def execute_load():
    mydb = get_connection()
    if not mydb:
        return

    try:
        procedures = [
            "load_dim_entidade",
            "load_dim_detalhes_contratos",
            "load_dim_cpv_contratos",
            "load_fact"
        ]

        for proc in procedures:
            logger.info(f"A executar: {proc}")
            log_id = change_status(None,'t_logs_carregamento',proc,"INICIO")
            # Cursor fresco por procedure — sem estado partilhado
            cur = mydb.cursor()
            try:
                cur.callproc(proc)

                # Drena todos os result sets
                for result in cur.stored_results():
                    try:
                        result.fetchall()
                    except Exception:
                        pass

                while cur.nextset():
                    pass

                mydb.commit()
                change_status(log_id, 't_logs_carregamento', None, "SUCESSO")
                logger.success(f"Concluído: {proc}")

            except mysql.connector.Error as e:
                logger.error(f"Erro em {proc}: {e}")
                change_status(log_id, 't_logs_carregamento', None, "ERRO", mensagem=str(e))
                

            finally:
                cur.close()

        logger.info("Transformação concluída com sucesso!")

    except mysql.connector.Error as e:
        logger.error(f"Erro na transformação: {e}")
    finally:
        mydb.close()



def get_table_columns(cursor, table_name: str) -> list:
    cursor.execute(f"SHOW COLUMNS FROM {table_name}")
    return [row[0] for row in cursor.fetchall()]

def insert_data_table(table_name: str, values: list, batch_size: int = 2000):
    if not values:
        logger.warning(f"Nenhuns dados para inserir na tabela {table_name}")
        return

    mydb = get_connection()
    mycursor = mydb.cursor()

    #Vai buscar as colunas da tabela
    table_columns = get_table_columns(mycursor, table_name)
    columns = [col for col in values[0].keys() if col in table_columns]
    placeholders = ", ".join(["%s"] * len(columns))
    cols_str = ", ".join(columns)

    sql = f"INSERT INTO {table_name} ({cols_str}) VALUES ({placeholders})"

    try:
        for i in range(0, len(values), batch_size):
            batch = values[i:i + batch_size]
            data = [tuple(r[col] for col in columns) for r in batch]
            mycursor.executemany(sql, data)
            mydb.commit()
            logger.info(f"Inseridos {min(i + batch_size, len(values))}/{len(values)} registos em {table_name}")
    except mysql.connector.Error as e:
        logger.error(f"Erro ao inserir em {table_name}: {e}")
    finally:
        mycursor.close()
        mydb.close()

#Para verificar se o valor é nulo ou não
def sanitize(value):
    if isinstance(value, float) and math.isnan(value):
        return None
    return value

#Para ver a ultima data extraida
#Caso aconteça algo e não de para extrair os dados
#Talvez fazer uma base de dados para isto
def get_last_date_extracted():
    return 'data'

#Selecionar os novos campos na base de dados
def get_distinct_data(nome_campo:str,table_name:str):
    #Check if any table is save in database
    mydb=get_connection()
    mycursor = mydb.cursor()
    #Para prevenir que é a base de dados que queremos
    query =f"SELECT DISTINCT {nome_campo} FROM {table_name};"
    mycursor.execute(query)
    data=data = [row[0] for row in mycursor.fetchall()]
    return data

def change_status(id: int | None,table_logs:str, nome_objeto: str | None, status: str, mensagem: str = None) -> int | None:
    mydb = get_connection()
    mycursor = mydb.cursor()
    match status:
        case "INICIO":
            query = "INSERT INTO "+table_logs+" (nome_objeto, status) VALUES (%s, 'INICIO')"
            mycursor.execute(query, (nome_objeto,))
            mydb.commit()
            return mycursor.lastrowid  # retorna o id do novo registo

        case "SUCESSO":
            query = "UPDATE "+table_logs+" SET status = 'SUCESSO', ultima_extracao = NOW() WHERE id = %s"
            mycursor.execute(query, (id,))
            mydb.commit()

        case "ERRO":
            query = "UPDATE "+table_logs+" SET status = 'ERRO', mensagem = %s, ultima_extracao = NOW() WHERE id = %s"
            mycursor.execute(query, (mensagem, id)) 
            mydb.commit()

        case _:
            logger.warning(f"Status desconhecido: {status}")

    mycursor.close()
    mydb.close()
    return None

