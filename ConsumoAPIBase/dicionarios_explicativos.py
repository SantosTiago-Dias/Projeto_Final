import pandas as pd
import json
import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv('.env')

CONTRATOS_FILE = 'Ficheiros_extracao/contratos.csv'

client = Groq(api_key=os.getenv('API_KEY'))

# Cache por coluna
def get_cache_file(col_name):
    return f"cache_{col_name}.json"


def load_cache(col_name):

    cache_file = get_cache_file(col_name)

    if os.path.exists(cache_file):
        with open(cache_file, 'r', encoding='utf-8') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {}
    else:
        with open(cache_file, 'w', encoding='utf-8') as f:
            json.dump({}, f)

    return {}


def save_cache(col_name, cache):

    cache_file = get_cache_file(col_name)

    with open(cache_file, 'w', encoding='utf-8') as f:
        json.dump(cache, f, ensure_ascii=False, indent=4)


def get_explanation_smart(value, col_name, cache):

    # Ignorar valores vazios
    if pd.isna(value) or value == "":
        return None

    value = str(value)

    # Se já está no cache
    if value in cache:
        return cache[value]

    print(f"[{col_name}] Novo detetado: {value}. A gerar explicação...")

    prompt = f"""
    Gere uma explicação detalhada relativamente ao termo '{value}' no contexto de contratos públicos.

    REGRAS:
    Começa exatamente com: "{value}:"
    Máximo 125 palavras
    Forneça uma descrição clara e concisa, destacando os principais aspetos e características
    associadas a este termo.
    A explicação deve ser informativa e fácil de entender,
    evitando ao maximo palavras complexas ou juridicas,
    adequada para alguém que não tem conhecimento prévio sobre o assunto.

    FORMATO:
    {value}: explicação simples.
    """

    try:

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        explanation = response.choices[0].message.content.strip()

    except Exception as e:

        print(f"Erro ao gerar explicação para {value}: {e}")
        explanation = "termo geral relacionado com contratos públicos"

    # Guardar no cache
    cache[value] = explanation
    save_cache(col_name, cache)

    return explanation


def main():

    # Carregar CSV
    df = pd.read_csv(CONTRATOS_FILE, sep=';')

    # Colunas a processar
    columns = [
        'contractingProcedureType',
        'contractTypes',
        'nonWrittenContractJustificationTypes',
    ]

    for col in columns:

        print(f"\nA processar coluna: {col}")

        # carregar cache dessa coluna
        cache = load_cache(col)

        # Evita valores repetidos
        unique_items = df[col].drop_duplicates()

        for value in unique_items:
            get_explanation_smart(value, col, cache)

        print(f"Tamanho cache {col}: {len(cache)}")

    print("\nExplicações completas.")


if __name__ == "__main__":
    main()