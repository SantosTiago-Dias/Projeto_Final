import pdfplumber
import pandas as pd
import re

registos = []

artigo = None
numero = None
alinea = None
subalinea = None

texto_artigo = ""
texto_numero = ""
texto_alinea = ""
texto_subalinea = ""

def guardar_registo():
    global texto_artigo, texto_numero, texto_alinea, texto_subalinea

    texto_completo = ""
    if texto_artigo.strip():
        texto_completo += texto_artigo.strip() + " "
    if texto_numero.strip():
        texto_completo += texto_numero.strip() + " "
    if texto_alinea.strip():
        texto_completo += texto_alinea.strip() + " "
    if texto_subalinea.strip():
        texto_completo += texto_subalinea.strip()

    if texto_completo.strip():
        registos.append({
            "artigo": artigo,
            "numero": numero,
            "alinea": alinea,
            "subalinea": subalinea,
            "texto": texto_completo.strip()
        })

# Ler PDF ccp e extrair dados
with pdfplumber.open("ccp.pdf") as pdf:
    for page in pdf.pages[16:196]:
        texto = page.extract_text()
        if not texto:
            continue

        for linha in texto.split("\n"):
            linha = linha.strip()
            if not linha:
                continue

            art = re.match(r"Artigo\s+(\d+\.º(?:-[A-Z])?)", linha)
            if art:
                guardar_registo()
                artigo = art.group(1)
                numero = alinea = subalinea = None
                texto_artigo = linha
                texto_numero = texto_alinea = texto_subalinea = ""
                continue

            num = re.match(r"^(\d{1,3})\s*-\s*(.*)", linha)
            if num:
                guardar_registo()
                numero = int(num.group(1))
                alinea = subalinea = None
                texto_numero = num.group(2)
                texto_alinea = texto_subalinea = ""
                continue

            sub = re.match(r"(i{1,3}|iv|v|vi{0,3})\)\s*(.*)", linha)
            if sub and artigo:
                guardar_registo()
                subalinea = sub.group(1)
                texto_subalinea = sub.group(2)
                continue

            ali = re.match(r"([a-hj-z])\)\s*(.*)", linha)
            if ali and artigo:
                guardar_registo()
                alinea = ali.group(1)
                subalinea = None
                texto_alinea = ali.group(2)
                texto_subalinea = ""
                continue

            # Acumular texto
            if subalinea:
                texto_subalinea += " " + linha
            elif alinea:
                texto_alinea += " " + linha
            elif numero:
                texto_numero += " " + linha
            elif artigo:
                texto_artigo += " " + linha

# Guardar último
guardar_registo()

df = pd.DataFrame(registos)

# Criar referência formatada
def formatar_referencia(row):
    partes = []

    if pd.notna(row["artigo"]):
        partes.append(f"Artigo {row['artigo']}")

    if pd.notna(row["numero"]):
        partes.append(f"n.º {int(row['numero'])}")

    if pd.notna(row["alinea"]):
        partes.append(f"alínea {row['alinea']})")

    if pd.notna(row["subalinea"]):
        partes.append(f"subalínea {row['subalinea']})")

    return ", ".join(partes)

df["referencia"] = df.apply(formatar_referencia, axis=1)

# Guardar CSV
df.to_csv("ccp_por_artigo.csv", encoding="utf-8-sig", index=False)

print("CSV final criado: ccp_por_artigo.csv")