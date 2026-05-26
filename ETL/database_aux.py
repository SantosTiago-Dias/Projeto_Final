from dotenv import load_dotenv
from loguru import logger
import mysql.connector
from mysql.connector import Error
import os
import math
from datetime import datetime
import requests
import time


load_dotenv('.env')
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INIT = os.path.join(BASE_DIR, 'init.sql')
VIEWS = os.path.join(BASE_DIR, 'views.sql')

PROCEDURES = os.path.join(BASE_DIR, 'procedures.sql')
URL_NOMI = "https://nominatim.openstreetmap.org/search"
URL_NASA = "https://eonet.gsfc.nasa.gov/api/v3/events?status=all"

#Function to get a connection to the database using environment variables
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
        logger.info("Tabelas verificadas/criadas com sucesso.")

        #To generate the views from views.sql (if they don't exist)
        with open(VIEWS, 'r', encoding='utf-8') as f:
            sql = f.read()
            for statement in sql.split(';'):
                statement = statement.strip()
                if statement:
                    mycursor.execute(statement)
        logger.info("views verificadas/criadas com sucesso.")
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
        logger.info("Procedures verificadas/criadas com sucesso.")
        mydb.commit()

    except FileNotFoundError:
        logger.error("Ficheiro init.sql não encontrado")
        return False
    except mysql.connector.Error as e:
        logger.error(f"Erro: {e}")
        return False
    finally:
        mycursor.close()
        mydb.close()
   
#Function to execute the transformation procedures and lookup normalization
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
            log_id = change_status(None, 't_logs_transformacao', proc, "INICIO")
            cur = mydb.cursor()
            try:
                cur.callproc(proc)
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

        # --- Normalização ---
        normalizacoes = [
            ('detalhes_contratos_transf', 'descricao'),
            ('detalhes_contratos_transf', 'objeto'),
            ('entidade_transf', 'nome')
            # ('outra_tabela', 'outra_coluna')
        ]

        for tabela, coluna in normalizacoes:
            label = f"normalizar_lookup({tabela}.{coluna})"
            logger.info(f"A executar: {label}")
            log_id = change_status(None, 't_logs_transformacao', label, "INICIO")
            cur = mydb.cursor()
            try:
                cur.callproc('normalizar_lookup', [tabela, coluna])
                for result in cur.stored_results():
                    try:
                        result.fetchall()
                    except Exception:
                        pass
                while cur.nextset():
                    pass
                mydb.commit()
                change_status(log_id, 't_logs_transformacao', None, "SUCESSO")
                logger.success(f"Normalizado: {tabela}.{coluna}")
            except mysql.connector.Error as e:
                logger.error(f"Erro na normalização {tabela}.{coluna}: {e}")
                change_status(log_id, 't_logs_transformacao', None, "ERRO", mensagem=str(e))
            finally:
                cur.close()

        logger.info("Transformação concluída com sucesso!")

    except mysql.connector.Error as e:
        logger.error(f"Erro na transformação: {e}")
    finally:
        mydb.close()

#Function to execute the load procedures
def execute_load():
    mydb = get_connection()
    if not mydb:
        return

    try:
        procedures = [
            "load_dims_dict",
            "load_dim_entidade",
            "load_dim_detalhes_contratos",
            "load_dim_cpv_contratos",
            "load_fact",
        ]

        for proc in procedures:
            logger.info(f"A executar: {proc}")
            log_id = change_status(None,'t_logs_carregamento',proc,"INICIO")
            # New cursor for each procedure to avoid issues with multiple result sets
            cur = mydb.cursor()
            try:
                cur.callproc(proc)

                # Extract and discard all result sets to ensure the connection is ready for the next procedure
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

#Function to get the columns of a table
def get_table_columns(cursor, table_name: str) -> list:
    cursor.execute(f"SHOW COLUMNS FROM {table_name}")
    return [row[0] for row in cursor.fetchall()]

#Function to insert data in batches
def insert_data_table(table_name: str, values: list, batch_size: int = 2000):
    if not values:
        logger.warning(f"Nenhuns dados para inserir na tabela {table_name}")
        return

    mydb = get_connection()
    mycursor = mydb.cursor()

    #Get the columns of table
    table_columns = get_table_columns(mycursor, table_name)
    columns = [col for col in values[0].keys() if col in table_columns]

    #HACK: ON DUPLICATE KEY INGORES HIM
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

#Function to verify if value is NaN and return None if it is
def sanitize(value):
    if isinstance(value, float) and math.isnan(value):
        return None
    return value

#Function to get the average of contracts extracted per day
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

#Function to select distinct values from a column in the database
def get_distinct_data(nome_campo: str, table_name: str):
    
    mydb = get_connection()
    mycursor = mydb.cursor()

    query = f"SELECT DISTINCT {nome_campo} FROM {table_name};"
    mycursor.execute(query)
    rows = mycursor.fetchall()

    # If only one column requested, return flat list (keeps backward compatibility)
    if len(rows) == 0 or len(rows[0]) == 1:
        return [row[0] for row in rows]
    
    # Multiple columns: return list of tuples
    return rows

def getEntitynotFound():
    mydb = get_connection()
    mycursor = mydb.cursor()

    #Returns all ids from dim_entidade where nome is 'Não disponivel'
    query = f"SELECT id_entidade from dim_entidade where nome like 'Não disponivel';"
    mycursor.execute(query)
    rows = mycursor.fetchall()
    return [row[0] for row in rows]

def updateEntity(updated_data:str ,entity_id:int)->None:
    mydb = get_connection()
    mycursor = mydb.cursor()

    query = f"UPDATE dim_entidade set "+updated_data +" where id_entidade = %s"
    mycursor.execute(query, (entity_id,))
    mydb.commit()

#Function responsable for status management in the logs tables (t_logs_extract,t_logs_transformacao and t_logs_carregamento)
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

#Function to get the average of contracts extracted per day and insert it in the database
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

#Function responsable for generating the data dimension and populating it
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

#Function responsable for loading natural events into dim_data
def load_eventos_naturais():
    mydb = get_connection()
    if not mydb:
        return

    cursor = mydb.cursor()

    try:
        logger.info("A obter eventos da API EONET...")

        response = requests.get(URL_NASA)

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
        logger.error(f"Erro: carregar eventos naturais - {e}")
        change_status(None,'t_logs_carregamento','eventos_naturais',"ERRO", mensagem=str(e))


    finally:
        cursor.close()
        mydb.close()

#Get distrito from Nominatim API using the query (name of the entity or country)
def get_distrito_from_nominatim(query: str) -> str | None:
    try:
        params = {
            "q": query,
            "format": "json",
            "addressdetails": 1,
            "limit": 1
        }

        headers = {
            "User-Agent": "etl-project/1.0"
        }

        response = requests.get(URL_NOMI, params=params, headers=headers)

        if response.status_code != 200:
            return None

        data = response.json()

        if not data:
            return None

        address = data[0].get("address", {})
        return address.get("county")

    except Exception as e:
        logger.error(f"Erro: Nominatim - {e}")
        change_status(None,'t_logs_transformacao','get_distrito_from_nominatim',"ERRO", mensagem=str(e))

        return None


#Function to populate the distrito column in entidade_transf using Nominatim API and fallback to parsing the country field
def enrich_entidades_transf():
    mydb = get_connection()
    if not mydb:
        return

    cursor = mydb.cursor(dictionary=True)

    try:
        logger.info("A enriquecer entidades_transf com distrito...")

        query = """
        SELECT id_entidade, nome, pais, distrito
        FROM entidade_transf
        """
        cursor.execute(query)
        entidades = cursor.fetchall()

        updates = 0

        for ent in entidades:

            # have data → ignores
            if ent["distrito"] and ent["distrito"]!='N/A':
                continue

            nome = ent["nome"]
            morada = ent["pais"]

            distrito = None

            # try for name
            if nome:
                distrito = get_distrito_from_nominatim(nome)


            # fallback: second try for country
            if not distrito and morada:
                partes = [p.strip() for p in morada.split(",")]

                if len(partes) >= 2:
                    distrito = partes[1]  # ex: Évora
                else:
                    distrito = "N/A"

            # fallback final
            if not distrito:
                distrito = "N/A"

            update_sql = """
            UPDATE entidade_transf
            SET distrito = %s
            WHERE id_entidade = %s
            """

            cursor.execute(update_sql, (distrito, ent["id_entidade"]))
            updates += 1

            # HACK: for nom problems with too many requests in short time
            time.sleep(1)

        mydb.commit()
        logger.success(f"entidades_transf atualizada! {updates} registos")

    except Exception as e:
        logger.error(f"Erro: enrich entidades_transf - {e}")
        change_status(None,'t_logs_transformacao','enrich_entidades_transf',"ERRO", mensagem=str(e))

    finally:
        cursor.close()
        mydb.close()