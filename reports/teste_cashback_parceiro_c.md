# Relatório A/B — Teste Cashback Parceiro C

**Parceiro:** Parceiro C
**Período:** 2011-07-01 até 2011-08-14
**Arquivo analisado:** `data/dataset_03_parceiroC.csv`

## 1. Contexto

Análise das variantes de cashback para o Parceiro C.

A pergunta central é: **qual variante de cashback deve ser escalada para 100% do tráfego?**

## 2. Qualidade dos dados

- Linhas iniciais: 90
- Linhas válidas: 90
- Linhas removidas: 0
- Datas inválidas: 0
- Compradores inválidos: 0
- Comissão inválida: 0
- Cashback inválido: 0
- Vendas inválidas: 0

## 3. Resultado consolidado por variante

| Grupo | Dias | Compradores | GMV | Comissão | Cashback | Lucro bruto | Lucro médio/dia | Margem GMV | Cashback rate | Lucro/comprador |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Grupo 1 | 45 | 4.549 | R$ 1.738.460,00 | R$ 121.693,00 | R$ 86.924,00 | R$ 34.769,00 | R$ 772,64 | 2,00% | 5,00% | R$ 7,64 |
| Grupo 2 | 45 | 4.522 | R$ 1.685.235,00 | R$ 117.967,00 | R$ 117.967,00 | R$ 0,00 | R$ 0,00 | 0,00% | 7,00% | R$ 0,00 |

## 4. Probabilidade estimada de cada grupo ser o melhor

Foi usada simulação bootstrap com **lucro bruto diário médio** como métrica principal.

| Grupo | Probabilidade de ser o melhor | IC 95% lucro médio/dia |
|---|---:|---:|
| Grupo 1 | 100,00% | R$ 715,15 até R$ 829,00 |
| Grupo 2 | 0,00% | R$ 0,00 até R$ 0,00 |

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
