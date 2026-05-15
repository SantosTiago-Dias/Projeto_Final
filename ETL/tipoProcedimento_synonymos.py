import os
from cerebras.cloud.sdk import Cerebras, RateLimitError
from dotenv import load_dotenv
import dictonary_aux as dictionary
from loguru import logger
import database_aux as db
import time

load_dotenv(".env")
CCP_FILE = "Tipo_Procedimento.json"
TABLE_NAME = "tipo_procedimento_dictionary"
TABLE_LOGS = 't_logs_transformacao'
client = Cerebras(api_key=os.getenv('API_KEY'))

#Sedders
KNOWN_PROCEDURE_TYPES = {
    'Consulta Prévia': 'A entidade convida pelo menos 3 empresas para apresentarem propostas e escolhe a melhor.',
    'Ajuste Direto Regime Geral': 'A entidade escolhe uma empresa específica e negoceia diretamente com ela.',
    'Concurso público': 'Qualquer empresa pode concorrer.',
    'Concurso limitado por prévia qualificação': 'Primeiro as empresas enviam o currículo; só as melhores/mais capazes são convidadas a apresentar preço.',
    'Procedimento de negociação': 'A entidade senta-se à mesa com as empresas para regatear condições e preços antes de fechar o contrato.',
    'Diálogo concorrencial': 'Usado em projetos muito complexos onde a entidade precisa que as empresas ajudem a desenhar a solução ideal.',
    'Ao abrigo de acordo-quadro (art.º 258.º)': 'A compra é feita a uma empresa que já tem um contrato pré-assinado com o Estado para esse tipo de bens.',
    'Ao abrigo de acordo-quadro (art.º 259.º)': 'Faz-se um mini-concurso apenas entre as empresas que já pertencem ao acordo-quadro daquela categoria.',
    'Parceria para a inovação': 'A entidade trabalha em conjunto com uma empresa para criar um produto ou tecnologia que ainda não existe no mercado.',
    'Disponibilização de bens móveis': 'Processo para vender, alugar ou dar equipamentos, carros ou mobiliário que o Estado já não precisa.',
    'Serviços sociais e outros serviços específicos': 'Regras mais simples para contratar serviços de saúde, educação ou apoio social.',
    'Concurso de conceção simplificado': 'Um concurso rápido para escolher um projeto de arquitetura ou design de valor mais baixo.',
    'Concurso de ideias simplificado': 'Procuram-se ideias criativas para resolver um problema, com menos burocracia que o habitual.',
    'Consulta Prévia Simplificada': 'Uma consulta a várias empresas, mas com prazos muito apertados para ser mais rápida.',
    'Concurso público simplificado': 'Um concurso aberto a todos, mas com menos papéis e prazos de resposta mais curtos.',
    'Concurso limitado por prévia qualificação simplificado': 'Seleção de currículos e propostas feita de forma acelerada para ganhar tempo.',
    'Ajuste Direto Regime Geral ao abrigo do artigo 7º da Lei n.º 30/2021, de 21.05': 'Compra direta feita de forma mais rápida para projetos urgentes ou com fundos europeus (como o PRR).',
    'Consulta prévia ao abrigo do artigo 7º da Lei n.º 30/2021, de 21.05': 'Consulta a várias empresas com regras facilitadas para acelerar obras ou compras do PRR.',
    'Ajuste direto simplificado': 'Compras muito pequenas (até 5.000€) que se resolvem apenas com a fatura, sem contrato escrito.',
    'Ajuste direto simplificado ao abrigo da Lei n.º 30/2021, de 21.05': 'Compras rápidas de valor baixo feitas sob o regime especial de fundos europeus.',
    'Setores especiais – isenção parte II': 'Regras aplicadas a empresas de água, luz ou transportes que têm mais liberdade para contratar do que os ministérios.',
    'Contratação excluída II': 'Contratos que não precisam de seguir as regras normais do Estado (ex: segredos militares ou acordos entre câmaras municipais).'
}

#Prepare data for insertion in the database
def prepare_data(artigo:int,explain:str):
    data={
        'tipo':artigo,
        'descricao':explain,
    }
    return data

#Seed known procedure types and their explanations into the dictionary and database
def seed_procedures_types(log_id:int):
    try:
        for proc_type, explanation in KNOWN_PROCEDURE_TYPES.items():
                if not dictionary.verify_id_exists(CCP_FILE, proc_type):
                    dictionary.add_value(CCP_FILE, str(proc_type), explanation)
                    db.insert_data_table(TABLE_NAME, [prepare_data(proc_type, explanation)])
                    logger.info(f"Seeded known procedure type: {proc_type}")
    except Exception as e:
        logger.error(f"ERROR: {e}")
        db.change_status(log_id,TABLE_LOGS, None, "ERRO", mensagem=str(e))

#Function to check for new procedure types in the database and get explanations for them using the LLM
def new_types_procedures(log_id:int):
    procedureType_list_distinc=db.get_distinct_data('tipo_procedimento','contratos_transf')
    for proceduteType in procedureType_list_distinc:
        if not dictionary.verify_id_exists(CCP_FILE,proceduteType):
            retries = 0
            while retries < 5:
                try:
                    prompt = f"""Você é um sistema de classificação de compras públicas europeias.

                    Tipo de procidimento: {proceduteType}

                    Retorna EXATAMENTE UMA FRASE onde expliques esse arigo em liguagem corrente.

                    REGRAS ESTRITAS:
                    - Responda APENAS com a frase
                    - SEM explicações, SEM introduções, SEM numeração
                    - SEM quebras de linha, SEM pontuação extra
                    - SEM observações
                    - SEM mudança de linha
                    - TUDO EM LOWERCASE

                    FORMATO:
                    {proceduteType}: explicação simples.
                    """

                    response = client.chat.completions.create(
                        model="llama3.1-8b",
                        messages=[{"role": "user", "content": prompt}],
                        max_completion_tokens=100,
                    )
                    
                    explain = response.choices[0].message.content.strip()

                    dictionary.add_value(CCP_FILE,str(proceduteType),explain)
                    db.insert_data_table(TABLE_NAME,[prepare_data(proceduteType,explain)])
                    
                    time.sleep(0.3)  # polite delay between requests
                    break

                except RateLimitError:
                    wait = 30 * (2 ** retries)
                    logger.warning(f"Rate limit hit for '{proceduteType}'. Waiting {wait}s...")
                    time.sleep(wait)
                    retries += 1

                except Exception as e:
                    logger.error(f"ERROR: {e}")
                    db.change_status(log_id,TABLE_LOGS, None, "ERRO", mensagem=str(e))
                    break

#Main function to orchestrate the seeding of known procedure types and the discovery of new ones
def main():
    dictionary.verifiy_File_exists(CCP_FILE)
    log_id = db.change_status(None, TABLE_LOGS, TABLE_NAME, "INICIO")

    try:
        # Insert seed data
        logger.info("A iniciar população de dados fixos dos Tipos de Procedimento")
        seed_procedures_types(log_id)

        # For new data
        logger.info("A verificar novos Tipos de Procedimento na base de dados")
        new_types_procedures(log_id)

        logger.info("Fim de população dos tipos de procedimentos")
        db.change_status(log_id, TABLE_LOGS, None, "SUCESSO")

    except Exception as e:
        logger.error(f"ERRO: {e}")
        db.change_status(log_id, TABLE_LOGS, None, "ERRO", mensagem=str(e))


if __name__ == "__main__":
    main()