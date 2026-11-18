"""Ponto de entrada: execute `python main.py`."""
from pathlib import Path
import json

from src.calculadora import simular_solar_simples

from src.armazenamento import carregar_atendimentos, salvar_atendimentos, exportar_csv
from src.atendimento import realizar_atendimento
from src.conhecimento import carregar_conhecimento
from src.indicadores import exibir_indicadores

RAIZ = Path(__file__).resolve().parent
ARQUIVO_CONHECIMENTO = RAIZ / 'data' / 'conhecimento_ia.json'
ARQUIVO_ATENDIMENTOS = RAIZ / 'data' / 'atendimentos.json'
ARQUIVO_CSV = RAIZ / 'data' / 'atendimentos.csv'
ARQUIVO_EXEMPLOS = RAIZ / 'data' / 'parametros_exemplo.json'
ARQUIVO_APARELHOS = RAIZ / 'data' / 'eletrodomesticos.json'
ARQUIVO_FONTES = RAIZ / 'data' / 'fontes_pesquisa.json'


def main():
    try:
        base = carregar_conhecimento(ARQUIVO_CONHECIMENTO)
        atendimentos = carregar_atendimentos(ARQUIVO_ATENDIMENTOS)
    except (OSError, ValueError) as erro:
        print(f'Erro ao carregar os arquivos de dados: {erro}')
        return

    while True:
        print('\n=== ASSISTENTE DE ENERGIA ===')
        print('1 - Iniciar atendimento')
        print('2 - Ver indicadores dos atendimentos')
        print('3 - Exportar atendimentos para CSV')
        print('4 - Estimar economia solar (pela conta ou pelos aparelhos)')
        print('5 - Consultar fontes e referências')
        print('6 - Ver temas que a IA conhece')
        print('0 - Sair')
        try:
            opcao = input('Escolha uma opção: ').strip()
            if opcao == '1':
                registro = realizar_atendimento(base)
                atendimentos.append(registro)
                salvar_atendimentos(ARQUIVO_ATENDIMENTOS, atendimentos)
                print('Atendimento salvo no JSON.')
            elif opcao == '2':
                exibir_indicadores(atendimentos)
            elif opcao == '3':
                exportar_csv(ARQUIVO_CSV, atendimentos)
                print(f'{len(atendimentos)} atendimento(s) exportado(s) para {ARQUIVO_CSV}.')
            elif opcao == '4':
                with ARQUIVO_EXEMPLOS.open(encoding='utf-8') as arq:
                    exemplos = json.load(arq)
                with ARQUIVO_APARELHOS.open(encoding='utf-8') as arq:
                    catalogo = json.load(arq)
                simular_solar_simples(catalogo['aparelhos'], exemplos['residencia'])
            elif opcao == '5':
                with ARQUIVO_FONTES.open(encoding='utf-8') as arq:
                    fontes = json.load(arq)
                for dado in fontes.values():
                    print(f"\n{dado['titulo']}\n{dado['url']}\n{dado['observacao']}")
            elif opcao == '6':
                print('\nTÓPICOS DA BASE:')
                for item in base:
                    print(' -', item['tema'])
            elif opcao == '0':
                exportar_csv(ARQUIVO_CSV, atendimentos)
                print('CSV atualizado. Até logo!')
                break
            else:
                print('Opção inválida. Tente novamente.')
        except (EOFError, KeyboardInterrupt):
            print('\nEncerrando o programa...')
            exportar_csv(ARQUIVO_CSV, atendimentos)
            break
        except OSError as erro:
            print(f'Erro ao salvar os dados: {erro}')


if __name__ == '__main__':
    main()
