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

KNOWN_PROCEDURE_TYPES = {
    'Consulta Prévia': 'procedimento utilizado para obter informações e opiniões de potenciais fornecedores antes de lançar um processo de contratação formal.',
    'Ajuste Direto Regime Geral': 'procedimento simplificado para contratações de baixo valor, onde a entidade pública pode negociar diretamente com um fornecedor sem necessidade de competição.',
    'Concurso público': 'procedimento formal e competitivo para contratações de grande valor, onde os fornecedores apresentam propostas e a entidade pública seleciona a melhor oferta com base em critérios pré-definidos.',
    'Concurso limitado por prévia qualificação': 'procedimento onde apenas fornecedores pré-qualificados podem participar do concurso público, garantindo que apenas empresas com capacidade comprovada concorram.',
    'Procedimento de negociação': 'procedimento onde a entidade pública negocia diretamente com um ou mais fornecedores para obter as melhores condições, geralmente utilizado em situações específicas previstas na legislação.',
    'Diálogo concorrencial': 'procedimento que combina elementos de concurso público e negociação, permitindo que a entidade pública dialogue com os fornecedores para aprimorar as propostas antes da decisão final.',
    'Ao abrigo de acordo-quadro (art.º 258.º)': 'procedimento utilizado para contratações que se enquadram em acordos-quadro previamente estabelecidos, onde a entidade pública pode celebrar contratos com fornecedores selecionados sem necessidade de competição adicional.',
    'Ao abrigo de acordo-quadro (art.º 259.º)': 'procedimento utilizado para contratações que se enquadram em acordos-quadro previamente estabelecidos, onde a entidade pública pode celebrar contratos com fornecedores selecionados sem necessidade de competição adicional.',
    'Parceria para a inovação': 'procedimento destinado a promover a inovação, onde a entidade pública colabora com fornecedores para desenvolver soluções inovadoras que atendam às suas necessidades específicas.',
    'Disponibilização de bens móveis': 'procedimento utilizado para garantir a disponibilidade de bens móveis necessários para a execução de um contrato, permitindo que a entidade pública alugue ou adquira esses bens conforme necessário.',
    'Serviços sociais e outros serviços específicos': 'procedimento específico para a contratação de serviços sociais e outros serviços que exigem uma abordagem diferenciada devido à sua natureza particular.',
    'Concurso de conceção simplificado': 'procedimento simplificado para contratações de baixo valor, onde a entidade pública pode negociar diretamente com um fornecedor sem necessidade de competição.',
    'Concurso de ideias simplificado': 'procedimento simplificado para contratações de baixo valor, onde a entidade pública pode negociar diretamente com um fornecedor sem necessidade de competição.',
    'Consulta Prévia Simplificada': 'procedimento simplificado para contratações de baixo valor, onde a entidade pública pode negociar diretamente com um fornecedor sem necessidade de competição.',
    'Concurso público simplificado': 'procedimento simplificado para contratações de baixo valor, onde a entidade pública pode negociar diretamente com um fornecedor sem necessidade de competição.',
    'Concurso limitado por prévia qualificação simplificado': 'procedimento simplificado para contratações de baixo valor, onde a entidade pública pode negociar diretamente com um fornecedor sem necessidade de competição.',
    'Ajuste Direto Regime Geral ao abrigo do artigo 7º da Lei n.º 30/2021, de 21.05': 'procedimento simplificado para contratações de baixo valor, onde a entidade pública pode negociar diretamente com um fornecedor sem necessidade de competição, conforme previsto no artigo 7º da Lei n.º 30/2021, de 21.05.',
    'Consulta prévia ao abrigo do artigo 7º da Lei n.º 30/2021, de 21.05': 'procedimento simplificado para contratações de baixo valor, onde a entidade pública pode negociar diretamente com um fornecedor sem necessidade de competição, conforme previsto no artigo 7º da Lei n.º 30/2021, de 21.05.',
    'Ajuste direto simplificado': 'procedimento simplificado para contratações de baixo valor, onde a entidade pública pode negociar diretamente com um fornecedor sem necessidade de competição.',
    'Ajuste direto simplificado ao abrigo da Lei n.º 30/2021, de 21.05': 'procedimento simplificado para contratações de baixo valor, onde a entidade pública pode negociar diretamente com um fornecedor sem necessidade de competição, conforme previsto na Lei n.º 30/2021, de 21.05.',
    'Setores especiais – isenção parte II': 'procedimento específico para contratações em setores especiais, onde a entidade pública pode estar isenta de seguir os procedimentos tradicionais de contratação devido à natureza particular do setor em questão.',
    'Contratação excluída II': 'procedimento específico para contratações que estão excluídas dos procedimentos tradicionais de contratação, onde a entidade pública pode seguir um processo simplificado ou diferente devido à natureza particular da contratação em questão.',
}

def prepare_data(artigo:int,explain:str):
    data={
        'tipo':artigo,
        'descricao':explain,
    }
    return data

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