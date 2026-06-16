# Case resolvido — Teste Técnico Growth AI-Native | Méliuz

## 1. Abertura da apresentação

Este case foi resolvido como uma solução reutilizável para análise de testes A/B de cashback.  
O objetivo foi reduzir o tempo de análise manual, padronizar a decisão e gerar um histórico de experimentos.

A pergunta central foi:

> Qual variante de cashback devemos escalar para 100% do tráfego?

## 2. Entendimento do problema

O desafio não era apenas analisar um CSV isolado.  
A proposta foi criar uma solução que qualquer pessoa do time consiga usar para novos testes, apenas trocando o arquivo de entrada.

O teste avaliava dois pontos:

1. Capacidade de construção: solução reutilizável, parametrizada e robusta.
2. Capacidade analítica: leitura crítica dos dados e decisão acionável.

## 3. Arquitetura construída

A solução foi organizada em uma estrutura simples:

```txt
data/       -> datasets de entrada
src/        -> script principal de análise
reports/    -> relatórios executivos gerados
outputs/    -> tracker CSV e métricas consolidadas
prompts/    -> prompts para uso com IA
```

O script principal é:

```txt
src/analyze_ab_test.py
```

Ele recebe o caminho do arquivo CSV, nome do teste e descrição.

## 4. Como a solução é executada

Exemplo:

```bash
python src/analyze_ab_test.py --file data/dataset_01_parceiroA.csv --test-name "Teste Cashback Parceiro A" --description "Análise das variantes de cashback para o Parceiro A."
```

A mesma solução roda os três datasets sem alteração de código.

## 5. Tratamento dos dados

A solução faz:

- Leitura do CSV.
- Validação das colunas obrigatórias.
- Conversão de valores monetários em formato brasileiro.
- Conversão de datas.
- Remoção de linhas inválidas.
- Criação de métricas derivadas.

Exemplo de métrica derivada:

```txt
lucro_bruto = comissão - cashback
```

Essa métrica é essencial porque cashback é custo.  
Então não basta olhar apenas para GMV ou compradores.

## 6. Métricas calculadas

Para cada grupo, foram calculadas:

- Compradores totais.
- GMV.
- Comissão total.
- Cashback total.
- Lucro bruto.
- Lucro bruto médio diário.
- Margem sobre GMV.
- Cashback rate.
- Ticket médio.
- Lucro por comprador.

A métrica principal escolhida foi:

```txt
lucro bruto médio diário
```

Ela foi escolhida porque mede crescimento com eficiência financeira.

## 7. Validação estatística

Foi aplicado bootstrap para estimar a probabilidade de cada grupo ser o melhor em lucro bruto médio diário.

A lógica foi:

1. Sortear dias com reposição dentro de cada grupo.
2. Calcular a média de lucro de cada grupo.
3. Verificar qual grupo venceu.
4. Repetir o processo 10.000 vezes.
5. Estimar a probabilidade de cada variante ser vencedora.

## 8. Resultado — Parceiro A

Decisão:

```txt
Manter Grupo 1 como padrão e não escalar aumento de cashback.
```

Resumo:

- Grupo 1 teve maior lucro bruto médio diário.
- Grupo 2 e Grupo 3 geraram mais volume, mas consumiram mais margem.
- Probabilidade do Grupo 1 ser a melhor variante: 93,98%.

## 9. Resultado — Parceiro B

Decisão:

```txt
Manter Grupo 1 como padrão e não escalar aumento de cashback.
```

Resumo:

- Grupo 1 teve maior lucro bruto total.
- Grupo 2 e Grupo 3 performaram pior em compradores, GMV e margem.
- Probabilidade do Grupo 1 ser a melhor variante: 100%.

## 10. Resultado — Parceiro C

Decisão:

```txt
Manter Grupo 1 como padrão e não escalar aumento de cashback.
```

Resumo:

- Grupo 2 zerou lucro bruto, pois cashback foi igual à comissão.
- Grupo 1 foi o único grupo com margem positiva.
- Probabilidade do Grupo 1 ser a melhor variante: 100%.

## 11. Decisão final consolidada

Nos três testes, a recomendação final foi:

```txt
Não escalar aumento de cashback. Manter Grupo 1 como padrão.
```

A leitura de Growth é:

> Cashback maior pode aumentar volume em alguns cenários, mas neste case não compensou financeiramente. O Grupo 1 preserva margem e gera melhor lucro bruto.

## 12. Registro no tracker

A solução gera automaticamente:

```txt
outputs/ab_tests_tracker.csv
```

Esse arquivo funciona como planilha de acompanhamento dos testes rodados.

Cada linha contém:

- Nome do teste.
- Descrição.
- Parceiro.
- Período.
- Variantes.
- Resultado.
- Decisão.
- Variante recomendada.
- Probabilidade da melhor variante.

## 13. Como transformar em Google Sheets

1. Abrir Google Sheets.
2. Criar uma nova planilha chamada `Growth AB Tests Tracker`.
3. Importar o arquivo `outputs/ab_tests_tracker.csv`.
4. Compartilhar com acesso público de leitura.
5. Adicionar o link no README do repositório.

## 14. Uso de IA no fluxo

A IA foi usada como camada de apoio para:

- Estruturar a solução.
- Revisar lógica analítica.
- Gerar prompts de operação.
- Validar clareza do relatório executivo.
- Padronizar a documentação.

O código continua determinístico e reutilizável.  
A IA não substitui a análise; ela ajuda a acelerar e revisar o fluxo.

## 15. Limitações da análise

A principal limitação é que os datasets não possuem visitantes, sessões ou usuários expostos.

Por isso, a análise não calcula conversão real.

Para uma análise mais completa, seria importante ter:

- Usuários expostos por variante.
- Conversões por variante.
- Segmento de usuário.
- Canal de aquisição.
- Receita incremental.
- Retenção ou recompra.

## 16. Encerramento da apresentação

A entrega resolve o problema proposto porque:

- Analisa os 3 datasets sem mudar código.
- Gera decisão acionável.
- Registra resultados em tracker.
- Gera relatórios para gestão.
- Usa IA de forma prática no fluxo.
- Mantém arquitetura simples e reaproveitável.
