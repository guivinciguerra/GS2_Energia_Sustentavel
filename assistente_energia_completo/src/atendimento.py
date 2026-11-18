"""Interação de atendimento e medição de tempo."""
import time
from datetime import datetime

from .conhecimento import buscar_item, normalizar


def perguntar_sim_nao(mensagem):
    while True:
        valor = normalizar(input(mensagem).strip())
        if valor in ('s', 'sim'):
            return True
        if valor in ('n', 'nao'):
            return False
        print('Digite S para sim ou N para não.')


def pedir_nota():
    while True:
        try:
            valor = int(input('Nota de facilidade de uso (1 a 5): '))
            if 1 <= valor <= 5:
                return valor
        except ValueError:
            pass
        print('Digite um número inteiro de 1 a 5.')


def pedir_duvida(mensagem):
    while True:
        duvida = input(mensagem).strip()
        if duvida:
            return duvida
        print('A dúvida não pode ficar vazia.')


def realizar_atendimento(base):
    inicio = time.time()
    print('\n--- Novo atendimento ---')
    original = pedir_duvida('Qual é sua dúvida sobre energia? ')
    atual = original
    tentativas = 0
    encontrou = False
    ajudou = False
    while True:
        tentativas += 1
        item = buscar_item(atual, base)
        if item is None:
            print('\nNão encontrei resposta para essa dúvida.')
        else:
            encontrou = True
            print('\nResposta encontrada:', item['resposta'])
            if item.get('fontes'):
                print('Referências: ' + ', '.join(item['fontes']) + ' (consulte data/fontes_pesquisa.json)')
            ajudou = perguntar_sim_nao('Esta resposta ajudou? (S/N): ')
            if ajudou:
                break
            print('Você pode reformular sua pergunta.')
        if not perguntar_sim_nao('Deseja tentar novamente? (S/N): '):
            break
        atual = pedir_duvida('Reformule sua dúvida: ')

    nota = pedir_nota()
    tempo_segundos = round(time.time() - inicio, 1)
    print(f'Atendimento concluído em {tempo_segundos:.1f} segundo(s).')
    return {
        'data_hora': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'duvida': original,
        'encontrou': 'Sim' if encontrou else 'Não',
        'ajudou': 'Sim' if ajudou else 'Não',
        'tentativas': tentativas,
        'tempo_segundos': tempo_segundos,
        'facilidade': nota,
    }
