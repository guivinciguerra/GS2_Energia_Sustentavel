# Assistente de Energia — Pesquisa e Atendimento

## Integrantes

Guilherme Vinciguerra Carvalho - RM 571951
Marcos Peterson - RM: 573857

## Iniciar

```bash
python main.py
```

No Windows, pode usar `py main.py`. No Linux/macOS, `python3 main.py`.

## Estrutura do projeto

```text
assistente_energia_completo/
├── main.py
├── README.md
├── requirements.txt
├── src/
│   ├── atendimento.py        # Perguntas, feedback, tentativas, nota e tempo
│   ├── conhecimento.py       # Busca baseada nas frases-chave do JSON
│   ├── calculadora.py        # Fórmulas de geração, economia e retorno solar
│   ├── armazenamento.py      # Grava histórico e exporta csv.DictWriter
│   └── indicadores.py        # Resposta encontrada, ajudou, tempo, tentativas
├── data/
│   ├── conhecimento_ia.json  # Temas, frases-chave, respostas e IDs de fonte
│   ├── fontes_pesquisa.json  # Referências e URLs para verificação
│   ├── parametros_exemplo.json # Valores de exemplos editáveis
│   ├── eletrodomesticos.json  # Potências e tempo típico de uso dos aparelhos
│   ├── atendimentos.json     # Histórico (inicialmente vazio)
│   └── atendimentos.csv      # Exportado com csv.DictWriter
├── pesquisa/
│   └── fontes_renovaveis.md  # Texto da pesquisa, cálculos e referências
└── tests/
    ├── test_sistema.py
    └── test_renovaveis.py
```

## Menu

- **1 — Iniciar atendimento:** pergunta livre sobre energia; se houver frase-chave, fornece explicação e referências. Pergunta se ajudou, permite novas tentativas, registra tempo e nota de 1 a 5.
- **2 — Ver indicadores:** resposta encontrada (%), taxa ajudou (%), tempo médio, tentativas por atendimento, facilidade e dúvidas sem solução.
- **3 — Exportar CSV:** `data/atendimentos.csv`, por `csv.DictWriter`, em UTF-8-SIG e `;`.
- **4 — Simular economia solar:** escolha entre **(1) informar o consumo em kWh da conta de luz** ou **(2) estimar o consumo indicando quantidade de aparelhos e horas por dia**. Depois, veja a estimativa de economia mensal e anual e o tamanho aproximado do sistema solar.
- **5 — Consultar fontes:** lista títulos, URLs e explicação de cada referência.
- **6 — Ver temas:** mostra o que a base JSON sabe responder.
- **0 — Sair:** atualiza o CSV e encerra.

## Exemplos de perguntas

- Como funciona energia solar?
- Quais as vantagens da energia solar?
- Como usar energia renovável na escola ou no centro comunitário?
- O que é geração compartilhada?
- Como funciona um aquecedor solar de água?
- Quais as limitações da energia eólica?
- Como calcular economia solar? (o programa encaminha para a opção 4)
- Qual o prazo de retorno do investimento?
- Como calcular kWh de um equipamento?
- Como funciona um biodigestor?

## Simulação fácil para o público geral

Na opção **4**, há dois caminhos:

**Caminho 1 — Tenho minha conta de luz:** procure o número de **consumo em kWh** (não é o valor em R$) e digite esse número. Por exemplo, `250`.

**Caminho 2 — Não sei meu consumo:** responda quantas geladeiras, TVs, ventiladores, chuveiros, lâmpadas, aparelhos de ar-condicionado etc. existem e quantas horas por dia são utilizados. O sistema estima o consumo com as potências aproximadas de `data/eletrodomesticos.json`:

`consumo mensal (kWh) = quantidade × potência média (W) × horas por dia × 30 ÷ 1000`.

Exemplo: uma TV de 100 W usada quatro horas por dia: `1 × 100 × 4 × 30 ÷ 1000 = 12 kWh/mês`.

Depois dos dois caminhos, a simulação é igual: usa uma **meta didática de compensar 80% do consumo** e solicita uma tarifa efetiva evitável por kWh (possui valor ilustrativo predefinido) e, opcionalmente, o custo de instalação. Calcula `economia mensal = 0,8 × consumo × tarifa efetiva`, além da economia anual e do tamanho estimado de sistema fotovoltaico. A tarifa efetiva não é necessariamente igual à tarifa total da conta, devido às regras de compensação e custos remanescentes.

**Estimativas, não garantias:** a geladeira é aproximada pelo consumo médio ao longo do dia; o chuveiro varia conforme banho e temperatura; dispositivos podem ter modos diferentes. Para precisão maior, use o consumo real em kWh da conta. O resultado não é uma cotação de projeto nem desconta necessariamente toda a tarifa da fatura. Os valores sugeridos são hipóteses didáticas, **não médias medidas de residências brasileiras**.

## Exemplos matemáticos

Residência: `3 × 4,5 × 30 × 0,8 = 324 kWh/mês`; aproveitados `min(324,250)=250`; economia `250 × R$ 0,85 = R$ 212,50/mês`; anual `R$ 2.550`; retorno `R$ 14.000 / R$ 2.550 = 5,49 anos`.

Centro comunitário: `8 × 4,5 × 30 × 0,8 = 864 kWh/mês`; aproveitados `700`; economia `700 × R$ 0,85 = R$ 595/mês`; anual `R$ 7.140`; retorno `R$ 36.000 / R$ 7.140 = 5,04 anos`.

## Dados e indicadores

Atendimentos concluídos são salvos em `data/atendimentos.json`; a exportação CSV é atualizada pelo menu 3 ou ao sair. O tempo utiliza `inicio = time.time()` e `round(time.time() - inicio, 1)`; mede o atendimento completo, incluindo a nota final. A taxa de acerto usa a resposta do usuário se a informação *ajudou*, não apenas se foi encontrada.

## Testes

```bash
python -m unittest discover -s tests -v
```
