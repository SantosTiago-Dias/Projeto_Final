import pandas as pd
import json
import os
import re
from groq import Groq
from dotenv import load_dotenv

load_dotenv(".env")
API_KEY = os.getenv("API_KEY")

CONTRATOS_FILE = "Ficheiros_extracao/contratos.csv"
CCP_FILE = "ccp_por_artigo.csv"

client = Groq(api_key=API_KEY)

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


# Normalizar referência para cache
def normalize_reference_for_cache(reference):
    if not reference:
        return None

    artigo_match = re.search(r"Artigo\s+(\d+\.º(?:-[A-Z])?)", reference, re.IGNORECASE)
    numero_match = re.search(r"n\.º\s*(\d+)", reference, re.IGNORECASE)
    alinea_match = re.search(r"alínea\s*([a-z])", reference, re.IGNORECASE)
    subalinea_match = re.search(r"subalínea\s*([ivx]+)", reference, re.IGNORECASE)

    parts = []
    if artigo_match:
        parts.append(f"Artigo {artigo_match.group(1)}")
    if numero_match:
        parts.append(f"n.º {numero_match.group(1)}")
    if alinea_match:
        parts.append(f"alínea {alinea_match.group(1)}")
    if subalinea_match:
        parts.append(f"subalínea {subalinea_match.group(1)}")

    return " ".join(parts) if parts else None


# Extrair referência
def extract_reference_vectorized(text_series):
    artigo = text_series.str.extract(
        r"artigo\s+(\d+\.º(?:-[A-Z])?)", flags=re.IGNORECASE
    )[0]
    numero = text_series.str.extract(
        r"n\.º\s*(\d+)", flags=re.IGNORECASE
    )[0].astype(float)
    alinea = text_series.str.extract(
        r"(?:alínea\s*([a-z])|,\s*([a-z])\))", flags=re.IGNORECASE
    )
    alinea = alinea[0].fillna(alinea[1])
    subalinea = text_series.str.extract(
        r"subalínea\s*([ivx]+)", flags=re.IGNORECASE
    )[0]
    return artigo, numero, alinea, subalinea

def build_reference_vectorized(artigo, numero, alinea, subalinea):
    ref = artigo.copy().fillna("").astype(str)
    ref = "Artigo " + ref
    ref += numero.fillna("").apply(lambda x: f" n.º {int(x)}" if x != "" else "")
    ref += alinea.fillna("").apply(lambda x: f" alínea {x}" if x != "" else "")
    ref += subalinea.fillna("").apply(lambda x: f" subalínea {x}" if x != "" else "")
    return ref


# Buscar texto CCP por referência
def get_ccp_text_by_reference(ccp_df, reference):
    if not reference:
        return None

    artigo_match = re.search(r"Artigo\s+(\d+\.º(?:-[A-Z])?)", reference, re.IGNORECASE)
    numero_match = re.search(r"n\.º\s*(\d+)", reference, re.IGNORECASE)
    alinea_match = re.search(r"alínea\s*([a-z])", reference, re.IGNORECASE)
    subalinea_match = re.search(r"subalínea\s*([ivx]+)", reference, re.IGNORECASE)

    artigo = artigo_match.group(1).strip().lower() if artigo_match else None
    numero = int(numero_match.group(1)) if numero_match else None
    alinea = alinea_match.group(1).strip().lower() if alinea_match else None
    subalinea = subalinea_match.group(1).strip().lower() if subalinea_match else None

    df = ccp_df.copy()
    if artigo:
        df = df[df["artigo"].astype(str).str.lower().str.strip() == artigo]
    if numero is not None:
        df = df[df["numero"].fillna(-1).astype(int) == numero]
    if alinea:
        df = df[df["alinea"].astype(str).str.lower().str.strip() == alinea]
    if subalinea:
        df = df[df["subalinea"].astype(str).str.lower().str.strip() == subalinea]

    if len(df) == 0:
        return None

    textos = df["texto"].astype(str)
    if textos.str.contains(r"\(Revogado", case=False).all():
        return "(Revogado.)"
    textos = textos[~textos.str.contains(r"\(Revogado", case=False)]
    return " ".join(textos)


def build_prompt(reference, texto):
    return f"""
Explica o seguinte trecho do Código dos Contratos Públicos em linguagem simples.

REGRAS:
- Começa exatamente com: "{reference}:"
- Linguagem clara
- Explica apenas a ideia principal
- Máximo 120 palavras
- Substitui termos jurídicos ou técnicos por palavras mais simples ou explica-os brevemente entre parênteses
- Se o texto for "(Revogado.)" escreve: "Este artigo ficou sem efeito."

FORMATO:
{reference}: explicação simples.

TEXTO ORIGINAL:
{texto}
"""


def explain_article(reference, texto, cache, col_name):
    canonical_ref = normalize_reference_for_cache(reference)
    if canonical_ref in cache:
        return cache[canonical_ref]

    if texto is None:
        explanation = f"{canonical_ref}: Não existe esta referência no Código."
        cache[canonical_ref] = explanation
        save_cache(col_name, cache)
        return explanation

    if texto == "(Revogado.)":
        explanation = f"{canonical_ref}: Este artigo ficou sem efeito."
        cache[canonical_ref] = explanation
        save_cache(col_name, cache)
        return explanation

    prompt = build_prompt(canonical_ref, texto)
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
        )
        explanation = response.choices[0].message.content.strip()
        cache[canonical_ref] = explanation
        save_cache(col_name, cache)
        return explanation
    except Exception as e:
        print(f"Erro: {e}")
        explanation = f"{canonical_ref}: Não foi possível gerar explicação."
        cache[canonical_ref] = explanation
        save_cache(col_name, cache)
        return explanation

# Processar coluna
def process_column(contratos, column_name, ccp_df):
    cache = load_cache(column_name)
    text_series = contratos[column_name].astype(str)
    artigo, numero, alinea, subalinea = extract_reference_vectorized(text_series)
    contratos[f"{column_name}_reference"] = build_reference_vectorized(artigo, numero, alinea, subalinea)
    contratos[f"{column_name}_ccp_text"] = [get_ccp_text_by_reference(ccp_df, ref) for ref in contratos[f"{column_name}_reference"]]
    unique_refs = contratos[[f"{column_name}_reference", f"{column_name}_ccp_text"]].drop_duplicates()
    for _, row in unique_refs.iterrows():
        if row[f"{column_name}_ccp_text"]:
            explain_article(row[f"{column_name}_reference"], row[f"{column_name}_ccp_text"], cache, column_name)

def main():
    print("A carregar contratos...")
    contratos = pd.read_csv(CONTRATOS_FILE, sep=";", encoding="utf-8-sig")

    print("A carregar CCP...")
    ccp_df = pd.read_csv(CCP_FILE, encoding="utf-8-sig")

    columns = [
        "contractFundamentationType"
        #"nonWrittenContractJustificationTypes"
    ]

    for col in columns:
        print(f"\nA processar coluna: {col}")
        process_column(contratos, col, ccp_df)
        print(f"Cache guardado: cache_{col}.json")

    print("\nProcessamento concluído! Todos os caches atualizados.")

if __name__ == "__main__":
    main()