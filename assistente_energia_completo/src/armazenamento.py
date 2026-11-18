"""Persistência em JSON e exportação em CSV com csv.DictWriter."""
import csv
import json
from pathlib import Path

CAMPOS_CSV = [
    'data_hora', 'duvida', 'encontrou', 'ajudou',
    'tentativas', 'tempo_segundos', 'facilidade',
]


def carregar_atendimentos(caminho):
    caminho = Path(caminho)
    if not caminho.exists():
        return []
    with caminho.open(encoding='utf-8') as arquivo:
        dados = json.load(arquivo)
    if not isinstance(dados, list):
        raise ValueError('Os atendimentos devem estar em uma lista JSON.')
    return dados


def salvar_atendimentos(caminho, atendimentos):
    """Salva de forma atômica para reduzir risco de arquivo truncado."""
    caminho = Path(caminho)
    caminho.parent.mkdir(parents=True, exist_ok=True)
    temporario = caminho.with_suffix(caminho.suffix + '.tmp')
    with temporario.open('w', encoding='utf-8') as arquivo:
        json.dump(atendimentos, arquivo, ensure_ascii=False, indent=2)
        arquivo.write('\n')
    temporario.replace(caminho)


def exportar_csv(caminho, atendimentos):
    """Recria o CSV a partir do histórico JSON, sem duplicar registros."""
    caminho = Path(caminho)
    caminho.parent.mkdir(parents=True, exist_ok=True)
    with caminho.open('w', encoding='utf-8-sig', newline='') as arquivo:
        escritor = csv.DictWriter(arquivo, fieldnames=CAMPOS_CSV, delimiter=';', extrasaction='ignore')
        escritor.writeheader()
        escritor.writerows(atendimentos)
    return caminho
