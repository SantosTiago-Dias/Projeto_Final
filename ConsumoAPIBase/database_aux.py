from dotenv import load_dotenv
from loguru import logger
import mysql.connector
import os
import math

load_dotenv('.env')

def get_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )

def verify_database_exists():
    #Check if any table is save in database
    mydb=get_connection()
    mycursor = mydb.cursor()
    #Para prevenir que é a base de dados que queremos
    mycursor.execute(f"USE {os.getenv("DB_NAME")}")
    mycursor.execute("SHOW TABLES")

    tables = mycursor.fetchall()

    if not tables:
        logger.info("Tabela de dados não existem")
        logger.info(f"Base de dados:{os.getenv("DB_NAME")}")
        try:
           with open('../Database/init.sql', 'r') as f:
            sql=f.read()
            for statement in sql.split(';'):
                statement = statement.strip()
                if statement:  # skip empty strings
                    mycursor.execute(statement)

            mydb.commit()
            logger.info("Tabelas criadas com sucesso!")

        except FileNotFoundError:
            logger.error("Ficheiro init.sql não encontrado")
        except mysql.connector.Error as e:
            logger.error(f"Erro ao criar tabelas: {e}")
        finally:
            mycursor.close()
        return False
    else:
        logger.info("Tabela de dados ja existe")
        mycursor.close()
        return True


def insert_data_table(table_name:str,values:list,batch_size: int = 2000):
    if not values:
        logger.warning(f"Nenhuns dados para inserir na tabela {table_name}")
        return

    mydb = get_connection()
    mycursor = mydb.cursor()

    # Constroi as colunas e deixa todo dinamico pronto para qualquer tabela
    columns = list(values[0].keys())
    placeholders = ", ".join(["%s"] * len(columns))
    cols_str = ", ".join(columns)

    sql = f"INSERT INTO {table_name} ({cols_str}) VALUES ({placeholders})"

    # Controis uma lista de colunas todas pela mesma ordem e organiazção
    data = [tuple(r[col] for col in columns) for r in values]

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
def get_last_date_extracted():
    return 'data'