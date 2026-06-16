# Relatório A/B — Teste Cashback Parceiro A

**Parceiro:** Parceiro A
**Período:** 2011-01-01 até 2011-04-02
**Arquivo analisado:** `data/dataset_01_parceiroA.csv`

## 1. Contexto

Análise das variantes de cashback para o Parceiro A.

A pergunta central é: **qual variante de cashback deve ser escalada para 100% do tráfego?**

## 2. Qualidade dos dados

- Linhas iniciais: 276
- Linhas válidas: 276
- Linhas removidas: 0
- Datas inválidas: 0
- Compradores inválidos: 0
- Comissão inválida: 0
- Cashback inválido: 0
- Vendas inválidas: 0

## 3. Resultado consolidado por variante

| Grupo | Dias | Compradores | GMV | Comissão | Cashback | Lucro bruto | Lucro médio/dia | Margem GMV | Cashback rate | Lucro/comprador |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Grupo 1 | 92 | 9.633 | R$ 5.605.173,00 | R$ 638.135,00 | R$ 233.424,00 | R$ 404.711,00 | R$ 4.399,03 | 7,11% | 4,08% | R$ 42,01 |
| Grupo 2 | 92 | 10.814 | R$ 6.423.096,00 | R$ 728.178,00 | R$ 370.659,00 | R$ 357.519,00 | R$ 3.886,08 | 5,60% | 5,59% | R$ 33,06 |
| Grupo 3 | 92 | 11.410 | R$ 6.785.856,00 | R$ 767.887,00 | R$ 503.600,00 | R$ 264.287,00 | R$ 2.872,68 | 4,40% | 6,79% | R$ 23,16 |

## 4. Probabilidade estimada de cada grupo ser o melhor

Foi usada simulação bootstrap com **lucro bruto diário médio** como métrica principal.

| Grupo | Probabilidade de ser o melhor | IC 95% lucro médio/dia |
|---|---:|---:|
| Grupo 1 | 93,98% | R$ 3.917,12 até R$ 4.931,90 |
| Grupo 2 | 6,02% | R$ 3.488,59 até R$ 4.315,82 |
| Grupo 3 | 0,00% | R$ 2.613,45 até R$ 3.155,89 |

## 5. Decisão recomendada

**Resultado:** Controle venceu

**Decisão:** Manter Grupo 1 como padrão e não escalar aumento de cashback

**Variante recomendada:** Grupo 1

**Racional:** O Grupo 1 teve o maior lucro bruto médio diário e melhor margem. As variantes com cashback maior trouxeram mais volume em alguns casos, mas reduziram o resultado financeiro.

## 6. Leitura executiva

O Grupo 3 gerou o maior GMV, mas o Grupo 1 gerou o melhor resultado econômico. Isso indica que aumentar cashback elevou volume, porém consumiu margem.

A recomendação prioriza **lucro bruto, margem e sustentabilidade financeira**, não apenas GMV ou quantidade de compradores.

## 7. Limitações

- O dataset não possui visitantes, sessões ou usuários expostos por variante. Portanto, não é possível calcular taxa de conversão real.
- A análise usa dados agregados por dia e por grupo.
- Para testes futuros, recomenda-se incluir usuários expostos, conversões, segmento e canal de aquisição.

## 8. Próxima ação

- Registrar o teste no tracker de experimentos.
- Se a empresa quiser testar cashback maior novamente, rodar novo teste com métrica de conversão e amostra balanceada.
- Monitorar lucro bruto e margem após qualquer mudança de tráfego.
