"""Cálculo dos indicadores exigidos pela atividade."""


def calcular_indicadores(atendimentos):
    total = len(atendimentos)
    if not total:
        return None
    encontradas = [r for r in atendimentos if r['encontrou'] == 'Sim']
    ajudaram = [r for r in atendimentos if r['ajudou'] == 'Sim']
    nao_resolvidas = [r['duvida'] for r in atendimentos if r['ajudou'] != 'Sim']
    return {
        'total': total,
        'respostas_encontradas_pct': 100 * len(encontradas) / total,
        'taxa_ajudou_pct': 100 * len(ajudaram) / total,
        # O tempo medido vai do início do atendimento até a nota final.
        # Média somente dos atendimentos em que uma resposta foi encontrada.
        'tempo_medio_segundos': (sum(float(r['tempo_segundos']) for r in encontradas) / len(encontradas)) if encontradas else None,
        'tentativas_por_atendimento': sum(int(r['tentativas']) for r in atendimentos) / total,
        'facilidade_media': sum(int(r['facilidade']) for r in atendimentos) / total,
        'duvidas_sem_solucao': nao_resolvidas,
    }


def exibir_indicadores(atendimentos):
    print('\n=== INDICADORES ===')
    dados = calcular_indicadores(atendimentos)
    if dados is None:
        print('Ainda não há atendimentos registrados.')
        return
    print(f"Total de atendimentos:        {dados['total']}")
    print(f"Resposta encontrada (%):      {dados['respostas_encontradas_pct']:.1f}%")
    print(f"Taxa de acerto: ajudou (%):   {dados['taxa_ajudou_pct']:.1f}%")
    tempo = dados['tempo_medio_segundos']
    print(f"Tempo médio para encontrar:  {tempo:.1f} s" if tempo is not None else 'Tempo médio para encontrar:  N/D')
    print(f"Tentativas por atendimento:  {dados['tentativas_por_atendimento']:.2f}")
    print(f"Facilidade de uso (1 a 5):   {dados['facilidade_media']:.2f}")
    print('\nDúvidas sem solução:')
    if dados['duvidas_sem_solucao']:
        for i, duvida in enumerate(dados['duvidas_sem_solucao'], 1):
            print(f'  {i}. {duvida}')
    else:
        print('  Nenhuma.')
