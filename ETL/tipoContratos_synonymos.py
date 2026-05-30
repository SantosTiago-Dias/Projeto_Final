import os
from groq import Groq, RateLimitError
from dotenv import load_dotenv
import dictonary_aux as dictionary
from loguru import logger
import database_aux as db
import time

load_dotenv(".env")
TABLE_NAME = "tipo_contrato_dictionary"
CCP_FILE = "Tipo_Contrato.json"
TABLE_LOGS = 't_logs_transformacao'

client = Groq(api_key=os.getenv('GROQ_API_KEY'))

#Sedders
KNOWN_CONTRACT_TYPES = {
    'Aquisição de bens móveis': 'Compra de produtos e materiais, desde computadores e papelaria até veículos ou maquinaria.',
    'Aquisição de serviços': 'Contratação de tarefas ou especialistas, como limpeza, segurança, consultoria ou manutenção de software.',
    'Concessão de obras públicas': 'A entidade privada constrói uma obra (ex: uma autoestrada) e ganha o direito de a explorar e cobrar pelo seu uso durante anos.',
    'Concessão de serviços públicos': 'Um privado fica responsável por gerir um serviço público (ex: águas ou transportes municipais) em nome do Estado.',
    'Empreitadas de obras públicas': 'Contrato para fazer uma obra específica, como construir uma escola, alcatroar uma rua ou reparar uma ponte.',
    'Locação de bens móveis': 'Aluguer de equipamentos ou veículos. A entidade paga para usar, mas o bem não passa a ser dela.',
    'Sociedade': 'Criação de uma parceria ou empresa mista entre o Estado e privados para gerir um projeto ou negócio em conjunto.',
    'Outros': 'Contratos que, pela sua natureza muito específica ou rara, não encaixam nas categorias acima.',
}

#Prepare data for insertion in the database
def prepare_data(artigo: str, explain: str):
    return {
        'tipo': artigo,
        'descricao': explain,
    }

#Function to seed known contract types into the database and dictionary file
def seed_contract_types(log_id: int):
    try:
        for contract_type, explanation in KNOWN_CONTRACT_TYPES.items():
            if not dictionary.verify_id_exists(CCP_FILE, contract_type):
                dictionary.add_value(CCP_FILE, str(contract_type), explanation)
                db.insert_data_table(TABLE_NAME, [prepare_data(contract_type, explanation)])
                logger.info(f"Seeded known contract type: {contract_type}")
    except Exception as e:
        logger.error(f"ERROR: {e}")
        db.change_status(log_id, TABLE_LOGS, None, "ERRO", mensagem=str(e))


#Function to check for new contract types in the database and generate explanations for them using the LLM
def new_types_contracts(log_id: int):
    contract_type_list = db.get_distinct_data('tipo_contrato', 'contratos_transf')

    for contract_type in contract_type_list:
        if not dictionary.verify_id_exists(CCP_FILE, contract_type):
            retries = 0
            while retries < 5:
                try:
                    prompt = f"""Você é um sistema de classificação de compras públicas europeias.

                    Tipo de contrato: {contract_type}

                    Retorna EXATAMENTE UMA FRASE onde expliques esse artigo em linguagem corrente.

                    REGRAS ESTRITAS:
                    - Responda APENAS com a frase
                    - SEM explicações, SEM introduções, SEM numeração
                    - SEM quebras de linha, SEM pontuação extra
                    - SEM observações
                    - SEM mudança de linha
                    - TUDO EM LOWERCASE

                    FORMATO:
                    {contract_type}: explicação simples.
                    """

                    response = client.chat.completions.create(
                        model="llama-3.1-8b-instant",
                        messages=[{"role": "user", "content": prompt}],
                        temperature=0.2,
                    )

                    explain = response.choices[0].message.content.strip()

                    dictionary.add_value(CCP_FILE, str(contract_type), explain)
                    db.insert_data_table(TABLE_NAME, [prepare_data(contract_type, explain)])

                    time.sleep(0.3)
                    break

                except RateLimitError:
                    wait = 30 * (2 ** retries)
                    logger.warning(f"Rate limit hit for '{contract_type}'. Waiting {wait}s...")
                    time.sleep(wait)
                    retries += 1

                except Exception as e:
                    logger.error(f"ERROR: {e}")
                    db.change_status(log_id, TABLE_LOGS, None, "ERRO", mensagem=str(e))
                    break

#Main function to orchestrate the seeding and checking for new contract types
def main():
    dictionary.verifiy_File_exists(CCP_FILE)
    log_id = db.change_status(None, TABLE_LOGS, TABLE_NAME, "INICIO")

    try:
        logger.info("A iniciar população de dados fixos dos Tipos de Contrato")
        seed_contract_types(log_id)

        logger.info("A verificar novos Tipos de Contrato na base de dados")
        new_types_contracts(log_id)

        logger.info("Fim de população dos tipos de contrato")
        db.change_status(log_id, TABLE_LOGS, None, "SUCESSO")

    except Exception as e:
        logger.error(f"ERRO: {e}")
        db.change_status(log_id, TABLE_LOGS, None, "ERRO", mensagem=str(e))


if __name__ == "__main__":
    main()