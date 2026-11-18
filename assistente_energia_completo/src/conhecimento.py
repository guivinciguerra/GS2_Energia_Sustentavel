"""Busca local por frases-chave em JSON; não é um LLM."""
import json
import re
import unicodedata
from pathlib import Path


def normalizar(texto):
    texto = unicodedata.normalize('NFD', str(texto).casefold())
    return ''.join(c for c in texto if unicodedata.category(c) != 'Mn')


def carregar_conhecimento(caminho):
    with Path(caminho).open(encoding='utf-8') as arquivo:
        base = json.load(arquivo)
    if not isinstance(base, list):
        raise ValueError('A base de conhecimento deve ser uma lista JSON.')
    for item in base:
        if (not isinstance(item, dict)
                or not isinstance(item.get('palavras_chave'), list)
                or not isinstance(item.get('resposta'), str)):
            raise ValueError('Item inválido na base de conhecimento.')
    return base


def buscar_item(pergunta, base):
    """Retorna o item que contém a frase-chave mais específica na pergunta."""
    pergunta_normalizada = normalizar(pergunta)
    pergunta_normalizada = re.sub(r'[^a-z0-9]+', ' ', pergunta_normalizada).strip()
    melhor = None
    pontuacao = 0
    for item in base:
        for termo in item['palavras_chave']:
            chave = re.sub(r'[^a-z0-9]+', ' ', normalizar(termo)).strip()
            if chave and re.search(r'(?<!\w)' + re.escape(chave) + r'(?!\w)', pergunta_normalizada):
                pontos = len(chave)
                if pontos > pontuacao:
                    melhor, pontuacao = item, pontos
    return melhor


def buscar_resposta(pergunta, base):
    item = buscar_item(pergunta, base)
    return item['resposta'] if item else None
