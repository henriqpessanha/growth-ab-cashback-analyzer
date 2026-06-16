# Growth A/B Cashback Analyzer — Case Méliuz

Solução reutilizável para análise de testes A/B de cashback.

## Objetivo

Responder à pergunta:

> Dado esse teste A/B, qual variante de cashback devemos escalar para 100% do tráfego?

A solução lê um CSV com o schema informado no teste, limpa os dados, calcula métricas por variante, estima a probabilidade de cada grupo ser o melhor usando bootstrap, gera relatório em Markdown e registra o resultado em um tracker CSV compatível com Google Sheets.

## Tecnologias

- Python
- Pandas
- NumPy
- Matplotlib
- Markdown
- CSV para tracker de experimentos
- Fluxo apoiado por IA com ChatGPT, Cursor, Claude Code ou Gemini

## Estrutura

```txt
growth-ab-analyzer-case/
├── data/
├── outputs/
├── prompts/
├── reports/
│   └── charts/
├── src/
│   └── analyze_ab_test.py
├── CASE_APRESENTACAO_PASSO_A_PASSO.md
├── README.md
└── requirements.txt
```

## Instalação

```bash
pip install -r requirements.txt
```

## Como rodar

Parceiro A:

```bash
python src/analyze_ab_test.py --file data/dataset_01_parceiroA.csv --test-name "Teste Cashback Parceiro A" --description "Análise das variantes de cashback para o Parceiro A."
```

Parceiro B:

```bash
python src/analyze_ab_test.py --file data/dataset_02_parceiroB.csv --test-name "Teste Cashback Parceiro B" --description "Análise das variantes de cashback para o Parceiro B."
```

Parceiro C:

```bash
python src/analyze_ab_test.py --file data/dataset_03_parceiroC.csv --test-name "Teste Cashback Parceiro C" --description "Análise das variantes de cashback para o Parceiro C."
```

## Saídas

- Relatórios executivos em `reports/`
- Gráficos em `reports/charts/`
- Tracker de experimentos em `outputs/ab_tests_tracker.csv`
- Resumo consolidado em `outputs/resumo_metricas_todos_testes.csv`

## Resultado final dos datasets fornecidos

| Teste | Decisão |
|---|---|
| Parceiro A | Manter Grupo 1 como padrão e não escalar aumento de cashback |
| Parceiro B | Manter Grupo 1 como padrão e não escalar aumento de cashback |
| Parceiro C | Manter Grupo 1 como padrão e não escalar aumento de cashback |

## Justificativa

Nos três datasets, o Grupo 1 apresentou maior lucro bruto médio diário e melhor margem. Algumas variantes com cashback maior aumentaram compradores ou GMV, mas reduziram a eficiência econômica.

## Limitações

O dataset não contém visitantes, sessões ou usuários expostos por variante. Por isso, não é possível calcular taxa de conversão real. A análise usa compradores, GMV e lucro bruto como métricas agregadas.

## Planilha de acompanhamento

O arquivo `outputs/ab_tests_tracker.csv` pode ser importado no Google Sheets e compartilhado com acesso público de leitura.
