from dotenv import load_dotenv
from loguru import logger
import mysql.connector
from mysql.connector import Error
import os
import math
from datetime import datetime
import requests


load_dotenv('.env')
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INIT = os.path.join(BASE_DIR, 'init.sql')
PROCEDURES = os.path.join(BASE_DIR, 'procedures.sql')

#Função para obter a connecção com a base de dados
def get_connection():
    try:
        return mysql.connector.connect(
            host=os.getenv("MYSQL_HOST", "database"),
            user=os.getenv("MYSQL_DB_USER", "root"),
            port=int(os.getenv("MYSQL_PORT", 3306)),
            password=os.getenv("MYSQL_ROOT_PASSWORD", ""),
            database=os.getenv("MYSQL_DATABASE", "ETL")
        )
    except Error as e:
        logger.error(f"Erro ao conectar à BD: {e}")
        raise SystemExit("Não foi possível conectar à base de dados. A encerrar...") from None
        
#Função para verificar se a base de dados existe e criar as tabelas e procedures necessárias
def verify_database_exists():
    mydb = get_connection()

    mycursor = mydb.cursor()
    try:

        mycursor.execute(f"USE {os.getenv('MYSQL_DATABASE')}")
        mycursor.execute("SHOW TABLES")
        mycursor.fetchall()

        #To generate the tables from init.sql (if they don't exist)
        with open(INIT, 'r', encoding='utf-8') as f:
            sql = f.read()
            for statement in sql.split(';'):
                statement = statement.strip()
                if statement:
                    mycursor.execute(statement)
        
        #To generate the procedures from procedures.sql (if they don't exist)
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
                        logger.warning(f"Error executing statement: {e}")
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
   
#Função para executar as procedures de transformação
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

#Função para executar as procedures de load
def execute_load():
    mydb = get_connection()
    if not mydb:
        return

    try:
        procedures = [
            "load_dim_entidade",
            "load_dim_detalhes_contratos",
            "load_dim_cpv_contratos",
            "load_fact",
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

        logger.info("Carregamento concluído com sucesso!")

    except mysql.connector.Error as e:
        logger.error(f"Erro no carregamento: {e}")
    finally:
        mydb.close()

#Função para obter as colunas de uma tabela
def get_table_columns(cursor, table_name: str) -> list:
    cursor.execute(f"SHOW COLUMNS FROM {table_name}")
    return [row[0] for row in cursor.fetchall()]

#Função para inserir dados em batch
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

    #HACK: Para prevenir contratos duplicados, usamos INSERT IGNORE.
    sql = f"""INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({', '.join(['%s'] * len(columns))}) ON DUPLICATE KEY UPDATE {', '.join([f"{col} = VALUES({col})" for col in columns])}"""

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

#Media de contratos extraidos por dia
def get_average_contracts_extracted()->float|None:
    mydb=get_connection()
    mycursor = mydb.cursor()

    try:
        query = "SELECT media_contratos FROM data_extracted ORDER BY id DESC LIMIT 1;"
        mycursor.execute(query)
        result = mycursor.fetchone()
        logger.info(f"Média de contratos extraídos por dia: {result[0] if result else 'N/A'}")
        if result:
            return float(result[0])
        else:
            return None
    except mysql.connector.Error as e:
        logger.error(f"Erro ao obter média de contratos extraídos: {e}")
        return None

#Selecionar os novos campos na base de dados
def get_distinct_data(nome_campo:str,table_name:str):
    
    mydb=get_connection()
    mycursor = mydb.cursor()

    #Para prevenir que é a base de dados que queremos
    query =f"SELECT DISTINCT {nome_campo} FROM {table_name};"
    mycursor.execute(query)
    data=data = [row[0] for row in mycursor.fetchall()]
    return data

#Mudar status dos logs
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
            if id is None:
                query = "INSERT INTO " + table_logs + " (status, nome_objeto, mensagem, ultima_extracao) VALUES ('ERRO', %s, %s, NOW())"
                mycursor.execute(query, (nome_objeto, mensagem))
            else:
                query = "UPDATE " + table_logs + " SET status = 'ERRO', mensagem = %s, ultima_extracao = NOW() WHERE id = %s"
                mycursor.execute(query, (mensagem, id))
            mydb.commit()

        case _:
            logger.warning(f"Status desconhecido: {status}")

    mycursor.close()
    mydb.close()
    return None

#Função para ir buscar a media de contratos extraidos
def average_extrated_contracts(num_contratos: int):
    mydb = get_connection()
    mycursor = mydb.cursor()

    try:
        insert_query = "INSERT INTO data_extracted (num_contratos) VALUES (%s)"
        mycursor.execute(insert_query, (num_contratos,))
        mydb.commit()

        last_id = mycursor.lastrowid
        logger.info(f"Número de contratos extraídos inseridos: {num_contratos} (ID: {last_id})")

        update_query = """
            UPDATE data_extracted
            SET media_contratos = (
                SELECT avg_val FROM (
                    SELECT AVG(num_contratos) AS avg_val FROM data_extracted
                ) AS tmp
            )
            WHERE id = %s
        """
        mycursor.execute(update_query, (last_id,))
        mydb.commit()

        mycursor.execute(
            "SELECT media_contratos FROM data_extracted WHERE id = %s", (last_id,)
        )
        average = mycursor.fetchone()[0]
        logger.info(f"Média de contratos extraídos por dia: {average:.2f}")

    except mysql.connector.Error as e:
        logger.error(f"Erro ao calcular a média de contratos extraídos: {e}")
    finally:
        mycursor.close()
        mydb.close()

#Função responsavel por gerar a dimensãpo data e populacionar
def ensure_dim_data():
    mydb=get_connection()
    start_date = '2026-01-01'
    end_date = '2036-12-31'

    if not mydb:
        change_status(None,'t_logs_carregamento','dim_data','ERRO', mensagem="Não foi possível conectar à base de dados para para gerar a dimensão data")
        return

    cur = None
    try:
        cur = mydb.cursor()
        cur.execute("SELECT COUNT(*) FROM dim_data")
        count = cur.fetchone()[0]

        
        #Count if dim_data has records. 
        # If it does, check the max year and extend if necessary. 
        # If it doesn't, generate from start_date to end_date.
        if count > 1:
            cur.execute("SELECT ano FROM dim_data WHERE ano IS NOT NULL ORDER BY chave_date DESC LIMIT 1")
            row = cur.fetchone()
            log_id = change_status(None,'t_logs_carregamento','dim_data',"INICIO")
            last_ano = int(row[0])
            today = datetime.today()

            if today.year >= last_ano:
                new_start = f"{last_ano + 1}-01-01"
                new_end   = f"{last_ano + 10}-12-31"
                try:
                    logger.info(f"A extender dim_data até {new_end}...")
                    cur.callproc('load_dim_data', [new_start, new_end])
                    mydb.commit()
                except Exception as e:
                    logger.error(f"Erro ao estender dim_data: {e}")
                    change_status(log_id, 't_logs_carregamento', None, "ERRO", mensagem=str(e))
        else:
            try:
                log_id = change_status(None,'t_logs_carregamento','dim_data',"INICIO")
                logger.info("dim_data vazia. A gerar calendário...")
                cur.callproc('load_dim_data', [start_date, end_date])
                mydb.commit()
                change_status(log_id, 't_logs_carregamento', None, "SUCESSO")
            except Exception as e:
                logger.error(f"Erro ao gerar calendário para dim_data: {e}")
                change_status(log_id, 't_logs_carregamento', None, "ERRO", mensagem=str(e))

        load_eventos_naturais()
    except Exception as e:
        logger.error(f"Erro ao garantir dim_data: {e}")
    finally:
        if cur:
            cur.close()
        if mydb:
            mydb.close()

#Função responsavel por carregar os eventos naturais na dim_data
def load_eventos_naturais():
    mydb = get_connection()
    if not mydb:
        return

    cursor = mydb.cursor()

    try:
        logger.info("A obter eventos da API EONET...")

        url = "https://eonet.gsfc.nasa.gov/api/v3/events?status=all"
        response = requests.get(url)

        if response.status_code != 200:
            logger.error(f"Erro na API: {response.status_code}")
            return

        data = response.json()
        updates = 0

        for event in data.get("events", []):
            titulo = event.get("title", "")

            # Filtrar para Portugal
            if "Portugal" not in titulo:
                continue

            for geo in event.get("geometry", []):
                data_evento = geo.get("date", "")[:10]

                if not data_evento:
                    continue

                sql = """
                UPDATE dim_data
                SET evento_natural = 
                    CASE 
                        WHEN evento_natural IS NULL THEN %s
                        ELSE CONCAT(evento_natural, ' | ', %s)
                    END
                WHERE data = %s
                  AND (
                        evento_natural IS NULL 
                        OR evento_natural NOT LIKE %s
                  )
                """

                like_pattern = f"%{titulo}%"

                cursor.execute(sql, (titulo, titulo, data_evento, like_pattern))
                updates += cursor.rowcount

        mydb.commit()
        logger.success(f"Eventos naturais (Portugal) carregados! Updates: {updates}")

    except Exception as e:
        logger.error(f"Erro ao carregar eventos naturais: {e}")

    finally:
        cursor.close()
        mydb.close()
