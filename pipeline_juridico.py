# --- Boot de bibliotecas ---
import re
import os
import spacy
import nltk
import pandas as pd
import numpy as np

# Carrega modelo do spaCy (baixa se necessário)
def _ensure_spacy_model(model_name="pt_core_news_sm"):
    try:
        return spacy.load(model_name)
    except OSError:
        import subprocess, sys, importlib
        subprocess.check_call([sys.executable, "-m", "spacy", "download", model_name])
        importlib.invalidate_caches()
        return spacy.load(model_name)

nlp = _ensure_spacy_model("pt_core_news_sm")

# Baixar recursos do NLTK
nltk.download("stopwords", quiet=True)
nltk.download("punkt", quiet=True)
from nltk.corpus import stopwords
STOP_PT = set(stopwords.words("portuguese"))

# --- Função 1: Limpeza de texto ---
def limpar_texto(texto: str, remover_stopwords: bool = False) -> str:
    texto = str(texto).lower()
    texto = re.sub(r'[^a-zà-ÿ\s]', '', texto, flags=re.IGNORECASE)
    texto = re.sub(r'\s+', ' ', texto).strip()
    if remover_stopwords:
        palavras = texto.split()
        texto = ' '.join([p for p in palavras if p not in STOP_PT])
    return texto

# --- Função 2: Sumarização ---
def sumarizar_texto(texto: str, n_sentencas: int = 3, usar_spacy: bool = False) -> str:
    if usar_spacy:
        doc = nlp(texto)
        sentencas = [sent.text.strip() for sent in doc.sents]
    else:
        nltk.download("punkt", quiet=True)
        from nltk.tokenize import sent_tokenize
        sentencas = sent_tokenize(texto, language="portuguese")
    if not sentencas:
        return texto.strip()
    return " ".join(sentencas[:n_sentencas])

# --- Função 3: Tradução de jargões ---
def traduzir_jargoes(texto: str) -> str:
    dicionario = {
        "litisconsórcio": "quando várias pessoas são parte em um processo",
        "jurisprudência": "conjunto de decisões de tribunais",
        "petição inicial": "primeiro documento de um processo",
        "ação rescisória": "ação que visa desfazer uma decisão judicial já tomada",
        "preclusão": "perda de um direito por não ter sido exercido no tempo certo",
    }
    for termo, explicacao in dicionario.items():
        padrao = re.compile(rf"\b({re.escape(termo)})\b", flags=re.IGNORECASE)
        texto = padrao.sub(f"[\\1: {explicacao}]", texto)
    return texto

# --- Função 4: Detecção de falácias ---
def detectar_falacias(texto: str) -> str:
    texto_lower = texto.lower()
    falacias_encontradas = []
    if "segundo especialistas" in texto_lower and "sem provas" in texto_lower:
        falacias_encontradas.append("🔸 Apelo à Autoridade: argumento baseado em autoridade sem evidência.")
    if "todo mundo sabe que" in texto_lower or "sempre acontece assim" in texto_lower:
        falacias_encontradas.append("🔸 Generalização Apressada: conclusão ampla com base em poucos casos.")
    if "eles acham que tudo é culpa do estado" in texto_lower:
        falacias_encontradas.append("🔸 Espantalho: distorção do argumento adversário para refutá-lo facilmente.")
    if "essa pessoa não entende nada" in texto_lower or "incompetente demais para opinar" in texto_lower:
        falacias_encontradas.append("🔸 Ad Hominem: ataque à pessoa em vez do argumento.")
    return falacias_encontradas if falacias_encontradas else "✅ Nenhuma falácia detectada com as heurísticas atuais."

# --- Função Final: Pipeline completo ---
def pipeline_juridico(texto_original: str, n_sentencas: int = 3) -> dict:
    texto_limpo = limpar_texto(texto_original)
    texto_traduzido = traduzir_jargoes(texto_limpo)
    resumo = sumarizar_texto(texto_traduzido, n_sentencas=n_sentencas, usar_spacy=True)
    falacias = detectar_falacias(texto_traduzido)

    return {
        "original": texto_original.strip(),
        "limpo": texto_limpo,
        "traduzido": texto_traduzido,
        "resumo": resumo,
        "falacias_detectadas": falacias
    }

if __name__ == "__main__":
    # --- Exemplo de uso ---
    exemplo = """
    Segundo especialistas, a decisão foi correta, mesmo sem apresentar provas. 
    A petição inicial já indicava litisconsórcio. Todo mundo sabe que sempre acontece assim.
    """
    resultado = pipeline_juridico(exemplo)

    # Exibir resultado formatado
    for k, v in resultado.items():
        print(f"\n🔹 {k.upper()}:\n{v}")
