# Relatório A/B — Teste Cashback Parceiro B

**Parceiro:** Parceiro B
**Período:** 2011-05-01 até 2011-06-30
**Arquivo analisado:** `data/dataset_02_parceiroB.csv`

## 1. Contexto

Análise das variantes de cashback para o Parceiro B.

A pergunta central é: **qual variante de cashback deve ser escalada para 100% do tráfego?**

## 2. Qualidade dos dados

- Linhas iniciais: 183
- Linhas válidas: 183
- Linhas removidas: 0
- Datas inválidas: 0
- Compradores inválidos: 0
- Comissão inválida: 0
- Cashback inválido: 0
- Vendas inválidas: 0

## 3. Resultado consolidado por variante

| Grupo | Dias | Compradores | GMV | Comissão | Cashback | Lucro bruto | Lucro médio/dia | Margem GMV | Cashback rate | Lucro/comprador |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Grupo 1 | 61 | 7.990 | R$ 4.093.818,00 | R$ 450.321,00 | R$ 163.751,00 | R$ 286.570,00 | R$ 4.697,87 | 7,00% | 4,00% | R$ 35,87 |
| Grupo 2 | 61 | 5.452 | R$ 2.863.019,00 | R$ 314.935,00 | R$ 171.778,00 | R$ 143.157,00 | R$ 2.346,84 | 5,00% | 6,00% | R$ 26,26 |
| Grupo 3 | 61 | 5.029 | R$ 2.629.963,00 | R$ 289.290,00 | R$ 236.697,00 | R$ 52.593,00 | R$ 862,18 | 2,00% | 9,00% | R$ 10,46 |

## 4. Probabilidade estimada de cada grupo ser o melhor

Foi usada simulação bootstrap com **lucro bruto diário médio** como métrica principal.

| Grupo | Probabilidade de ser o melhor | IC 95% lucro médio/dia |
|---|---:|---:|
| Grupo 1 | 100,00% | R$ 4.265,99 até R$ 5.214,94 |
| Grupo 2 | 0,00% | R$ 2.105,28 até R$ 2.639,63 |
| Grupo 3 | 0,00% | R$ 779,52 até R$ 960,22 |

## 5. Decisão recomendada

**Resultado:** Controle venceu

**Decisão:** Manter Grupo 1 como padrão e não escalar aumento de cashback

**Variante recomendada:** Grupo 1

**Racional:** O Grupo 1 teve o maior lucro bruto médio diário e melhor margem. As variantes com cashback maior trouxeram mais volume em alguns casos, mas reduziram o resultado financeiro.

## 6. Leitura executiva

O Grupo 1 concentrou o melhor resultado econômico e deve ser mantido como padrão.

A recomendação prioriza **lucro bruto, margem e sustentabilidade financeira**, não apenas GMV ou quantidade de compradores.

## 7. Limitações

- O dataset não possui visitantes, sessões ou usuários expostos por variante. Portanto, não é possível calcular taxa de conversão real.
- A análise usa dados agregados por dia e por grupo.
- Para testes futuros, recomenda-se incluir usuários expostos, conversões, segmento e canal de aquisição.

## 8. Próxima ação

- Registrar o teste no tracker de experimentos.
- Se a empresa quiser testar cashback maior novamente, rodar novo teste com métrica de conversão e amostra balanceada.
- Monitorar lucro bruto e margem após qualquer mudança de tráfego.
