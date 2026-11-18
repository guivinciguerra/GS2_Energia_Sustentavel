"""Estimativas didáticas; não calculam a fatura regulatória real."""
import math


def calcular_solar(potencia_kwp, horas_sol_pleno_dia, dias_mes, desempenho,
                   consumo_compensavel_kwh, valor_evitado_por_kwh_reais, investimento_reais):
    entradas = (potencia_kwp, horas_sol_pleno_dia, dias_mes, desempenho,
                consumo_compensavel_kwh, valor_evitado_por_kwh_reais, investimento_reais)
    if any(not math.isfinite(float(x)) for x in entradas):
        raise ValueError('Todos os valores devem ser finitos.')
    if any(float(x) < 0 for x in entradas):
        raise ValueError('Os valores não podem ser negativos.')
    if not 0 <= desempenho <= 1:
        raise ValueError('Desempenho deve estar entre 0 e 1.')
    if dias_mes <= 0 or dias_mes > 31 or horas_sol_pleno_dia > 24:
        raise ValueError('Verifique dias no mês e horas de sol pleno.')
    geracao = potencia_kwp * horas_sol_pleno_dia * dias_mes * desempenho
    aproveitado = min(geracao, consumo_compensavel_kwh)
    economia_mes = aproveitado * valor_evitado_por_kwh_reais
    economia_ano = economia_mes * 12
    retorno = investimento_reais / economia_ano if economia_ano > 0 else None
    return {'geracao_kwh_mes': geracao, 'energia_aproveitada_kwh_mes': aproveitado,
            'economia_reais_mes': economia_mes, 'economia_reais_ano': economia_ano,
            'retorno_simples_anos': retorno}


def pedir_numero(rotulo, padrao, minimo=0, maximo=None):
    while True:
        texto = input(f'{rotulo} [{padrao}]: ').strip().replace(',', '.')
        try:
            numero = float(texto) if texto else float(padrao)
            if not math.isfinite(numero) or numero < minimo or (maximo is not None and numero > maximo):
                raise ValueError
            return numero
        except ValueError:
            print('Valor inválido; informe um número dentro do intervalo.')


def simular_solar(parametros):
    print('\n=== SIMULADOR SOLAR (VALORES ILUSTRATIVOS) ===')
    print('Use parâmetros de sua residência/espaço comunitário. Enter aceita o exemplo.')
    rotulos = [
        ('potencia_kwp','Potência do sistema (kWp)',0,None),
        ('horas_sol_pleno_dia','Horas de sol pleno por dia',0,24),
        ('dias_mes','Dias considerados no mês',1,31),
        ('desempenho','Fator de desempenho (0 a 1)',0,1),
        ('consumo_compensavel_kwh','Consumo compensável máximo no mês (kWh)',0,None),
        ('valor_evitado_por_kwh_reais','Valor efetivamente evitável (R$/kWh)',0,None),
        ('investimento_reais','Investimento inicial (R$)',0,None),
    ]
    valores = {chave: pedir_numero(rotulo, parametros[chave], minimo, maximo)
               for chave, rotulo, minimo, maximo in rotulos}
    resultado = calcular_solar(**valores)
    print('\nFÓRMULAS E CONTAS:')
    print(f"Geração = {valores['potencia_kwp']:g} × {valores['horas_sol_pleno_dia']:g} × {valores['dias_mes']:g} × {valores['desempenho']:g} = {resultado['geracao_kwh_mes']:.2f} kWh/mês")
    print(f"Energia aproveitada = mínimo({resultado['geracao_kwh_mes']:.2f}, {valores['consumo_compensavel_kwh']:g}) = {resultado['energia_aproveitada_kwh_mes']:.2f} kWh/mês")
    print(f"Economia mensal = {resultado['energia_aproveitada_kwh_mes']:.2f} × R$ {valores['valor_evitado_por_kwh_reais']:.2f} = R$ {resultado['economia_reais_mes']:.2f}")
    print(f"Economia anual = R$ {resultado['economia_reais_mes']:.2f} × 12 = R$ {resultado['economia_reais_ano']:.2f}")
    if resultado['retorno_simples_anos'] is None:
        print('Retorno simples: não calculável (sem economia positiva).')
    else:
        print(f"Retorno simples = R$ {valores['investimento_reais']:.2f} ÷ R$ {resultado['economia_reais_ano']:.2f} = {resultado['retorno_simples_anos']:.2f} anos")
    print('ATENÇÃO: simulação educativa. Não representa proposta comercial nem fatura real.')
    print('Tarifa, créditos, impostos, custos remanescentes, sazonalidade e manutenção alteram a economia.')
    return resultado


def estimar_consumo_aparelhos(itens, dias_mes=30):
    """itens: lista de dicionários {nome, quantidade, potencia_media_w, horas_por_dia}."""
    if not 1 <= dias_mes <= 31:
        raise ValueError('Dias do mês inválidos.')
    detalhes = []
    for item in itens:
        quantidade = item['quantidade']
        potencia = item['potencia_media_w']
        horas = item['horas_por_dia']
        if (not all(math.isfinite(float(v)) for v in (quantidade, potencia, horas))
                or quantidade < 0 or int(quantidade) != quantidade or potencia < 0
                or not 0 <= horas <= 24):
            raise ValueError('Quantidade, potência ou tempo de uso inválido.')
        consumo = quantidade * potencia * horas * dias_mes / 1000
        detalhes.append({'nome': item['nome'], 'quantidade': int(quantidade),
                         'consumo_kwh_mes': round(consumo, 3)})
    return {'consumo_kwh_mes': round(sum(d['consumo_kwh_mes'] for d in detalhes), 3),
            'detalhes': detalhes}


def calcular_economia_por_consumo(consumo_kwh_mes, tarifa_efetiva, cobertura=0.8,
                                  sol_pleno_dia=4.5, desempenho=0.8,
                                  investimento_reais=0):
    """Dimensionamento didático de sistema que gere cobertura * consumo por mês."""
    valores = (consumo_kwh_mes, tarifa_efetiva, cobertura, sol_pleno_dia, desempenho, investimento_reais)
    if not all(math.isfinite(float(v)) for v in valores):
        raise ValueError('Use números válidos.')
    if (consumo_kwh_mes < 0 or tarifa_efetiva < 0 or investimento_reais < 0 or
            not 0 <= cobertura <= 1 or not 0 < sol_pleno_dia <= 24 or not 0 < desempenho <= 1):
        raise ValueError('Valores fora dos limites.')
    potencia_kwp = consumo_kwh_mes * cobertura / (sol_pleno_dia * 30 * desempenho)
    resultado = calcular_solar(potencia_kwp, sol_pleno_dia, 30, desempenho,
                              consumo_kwh_mes, tarifa_efetiva, investimento_reais)
    resultado.update({'consumo_kwh_mes': consumo_kwh_mes,
                      'cobertura': cobertura, 'potencia_necessaria_kwp': potencia_kwp,
                      'tarifa_efetiva': tarifa_efetiva})
    return resultado


def pedir_inteiro(rotulo, padrao=0, maximo=1000):
    while True:
        entrada = input(f'{rotulo} [{padrao}]: ').strip()
        if not entrada:
            return padrao
        try:
            numero = int(entrada)
            if 0 <= numero <= maximo:
                return numero
        except ValueError:
            pass
        print(f'Digite um número inteiro entre 0 e {maximo}.')


def obter_consumo_interativo(aparelhos):
    """Oferece consumo informado pela conta ou estimativa por aparelhos."""
    print('\nComo quer informar o consumo de energia?')
    print('1 - Digitar o consumo mensal em kWh (vem na conta de luz)')
    print('2 - Não sei: responder quantos aparelhos há na casa e quanto são usados')
    while True:
        modo = input('Escolha 1 ou 2: ').strip()
        if modo in ('1', '2'):
            break
        print('Escolha 1 ou 2.')
    if modo == '1':
        consumo = pedir_numero('Consumo mensal que aparece na conta (kWh)', 250, 0)
        return consumo, 'informado na conta de luz'

    itens = []
    print('\nInforme quantos aparelhos você tem. Aperte Enter para usar zero.')
    print('O tempo sugerido é uma média ilustrativa: você pode alterá-lo.')
    for aparelho in aparelhos:
        quantidade = pedir_inteiro(f"Quantidade de {aparelho['nome']}")
        if quantidade == 0:
            continue
        horas = pedir_numero(f"Horas de uso por dia de {aparelho['nome']}",
                            aparelho['horas_por_dia'], 0, 24)
        itens.append({**aparelho, 'quantidade': quantidade, 'horas_por_dia': horas})
    estimativa = estimar_consumo_aparelhos(itens)
    print('\nConsumo mensal estimado por aparelho:')
    for item in estimativa['detalhes']:
        print(f"- {item['nome']} ({item['quantidade']}): {item['consumo_kwh_mes']:.1f} kWh/mês")
    consumo = estimativa['consumo_kwh_mes']
    print(f'TOTAL estimado: {consumo:.1f} kWh por mês.')
    print('Essa estimativa pode ser menor que sua conta real, pois só inclui os aparelhos informados.')
    return consumo, 'estimado por aparelhos'


def simular_solar_simples(aparelhos, parametros):
    print('\n=== QUANTO EU PODERIA ECONOMIZAR COM ENERGIA SOLAR? ===')
    consumo, origem = obter_consumo_interativo(aparelhos)
    print(f'Consumo mensal ({origem}): {consumo:.1f} kWh.')
    tarifa = pedir_numero('Quanto vale cada kWh que pode ser economizado (R$)?',
                         parametros['valor_evitado_por_kwh_reais'], 0)
    print('Se você não souber esse valor, use o exemplo sugerido (não é tarifa oficial).')
    investimento = pedir_numero('Orçamento de instalação solar (R$; 0 se não souber)', 0, 0)
    resultado = calcular_economia_por_consumo(consumo, tarifa, investimento_reais=investimento)
    print('\n--- SUA ESTIMATIVA ---')
    print(f"Consumo atual aproximado: {consumo:.1f} kWh/mês")
    print('O exemplo considera energia solar para cobrir 80% desse consumo.')
    print(f"Energia solar estimada: {resultado['geracao_kwh_mes']:.1f} kWh/mês")
    print(f"Tamanho aproximado do sistema: {resultado['potencia_necessaria_kwp']:.2f} kWp")
    print(f"Economia mensal estimada: R$ {resultado['economia_reais_mes']:.2f}")
    print(f"Economia anual estimada: R$ {resultado['economia_reais_ano']:.2f}")
    print(f"Conta matemática: {resultado['energia_aproveitada_kwh_mes']:.1f} kWh × R$ {tarifa:.2f} = R$ {resultado['economia_reais_mes']:.2f}/mês")
    if investimento > 0 and resultado['retorno_simples_anos'] is not None:
        print(f"Retorno simples estimado: {resultado['retorno_simples_anos']:.1f} anos")
    print('\nIMPORTANTE: não é uma promessa de desconto ou cotação de instalação.')
    print('A conta continuará com possíveis cobranças fixas, tarifas de uso da rede, impostos e outros encargos.')
    print('A economia real depende de local, telhado, clima, tipo de conexão, horário de uso e regras de compensação.')
    return resultado
