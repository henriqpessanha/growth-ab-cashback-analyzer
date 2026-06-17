# **Relatório do Case da Méliuz**

Neste case, meu objetivo foi construir uma solução reutilizável para análise de testes A/B de cashback, simulando um problema real do time de Growth do Méliuz. A proposta não foi apenas analisar três arquivos CSV isolados. A minha intenção foi criar uma primeira versão de uma ferramenta que pudesse ser reaproveitada pelo time em novos testes, reduzindo tempo de análise, padronizando decisões e diminuindo o risco de interpretações diferentes para o mesmo tipo de experimento.

O desafio principal era responder a uma pergunta de negócio:

Dado um teste A/B de cashback, qual variante devemos escalar para 100% do tráfego?

Para responder isso de forma responsável, não considerei apenas volume de vendas ou quantidade de compradores. Em um contexto de cashback, vender mais nem sempre significa gerar melhor resultado. Uma variante pode aumentar o GMV, mas, ao mesmo tempo, distribuir cashback demais e reduzir a margem do negócio. Por isso, estruturei a análise considerando crescimento, custo do incentivo e eficiência financeira.

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

## **Como eu interpretei o problema do case?**

O Méliuz trabalha com cashback. Nesse modelo, existe uma relação direta entre incentivo e rentabilidade: “Quanto maior o cashback oferecido ao usuário, maior pode ser o estímulo para compra”. Porém, também maior será o custo da campanha. Com isso, eu interpretei que a melhor decisão de Growth não deveria ser baseada só na variante que gerou mais compradores ou mais vendas totais. A melhor decisão deveria considerar qual dos grupos trouxe o melhor equilíbrio entre crescimento e lucro. Em outras palavras, eu procurei responder qual variante gera um resultado de negócio mais sustentável dentre todas elas.

Essa distinção é importante porque Growth não é apenas crescer a qualquer custo. Growth eficiente é crescer preservando margem, aprendendo com dados e tomando decisões que possam ser repetidas com segurança. Quando se trata de Growth, o marketing mais básico (Pensar que as análises profundas e relatórios não importam, visando somente o lucro imediato e de curto prazo) não se mostra eficiente.

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

## **Qual foi a estratégia adotada?**

Minha estratégia foi dividir a solução em duas partes, sendo elas:

1. A construção de uma ferramenta que seja reutilizável.  
2. A análise crítica dos resultados dos testes.

A ferramenta foi construída em Python, utilizando bibliotecas voltadas para análise de dados. Ela recebe um arquivo CSV como entrada, trata os dados, calcula métricas, compara os grupos, gera um relatório e atualiza um tracker de acompanhamento.

A análise crítica foi feita em cima das métricas calculadas, considerando principalmente o lucro bruto e a margem de cada grupo.

Essa abordagem atende ao objetivo do teste porque não entrega apenas uma resposta pontual. Ela entrega um processo que pode ser repetido em novos testes.

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

## **Por que Python?**

Escolhi Python porque é uma linguagem muito utilizada para análise de dados, automação e criação de scripts reutilizáveis, além de ser uma linguagem de programação que eu acredito que seja simples de se aprender.

No caso do case, o python foi uma escolha adequada por três motivos:

- Permite ler arquivos CSV com facilidade.  
- Possui bibliotecas fortes para manipulação de dados, como Pandas e NumPy.  
- Facilita a criação de uma solução simples de rodar, inclusive por pessoas não técnicas, desde que tenham instruções claras no README.

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

## **Por que Pandas e NumPy?**

Usei Pandas para trabalhar com os datasets como se fossem tabelas.

O que consegui (usando Pandas):

* Ler os arquivos CSV;  
* Padronizar nomes de colunas;  
* Converter valores monetários;  
* Agrupar dados por grupo;  
* Somar comissão, cashback e vendas;  
* Calcular médias e margens;  
* Gerar arquivos de saída.

Usei NumPy para apoiar cálculos numéricos e simulações estatísticas, principalmente no bootstrap.

Essas duas bibliotecas são adequadas porque tornam a solução mais simples, rápida e confiável para análise de dados.

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

## **Como é que a solução foi organizada?**

Organizei o projeto com uma estrutura parecida com a de uma ferramenta interna real. A estrutura ficou separada por responsabilidade:

* A pasta `data` guarda os arquivos CSV;  
* A pasta `src` contém o código principal;  
* A pasta `reports` armazena os relatórios gerados;  
* A pasta `outputs` guarda o tracker consolidado;  
* A pasta `prompts` documenta como a solução pode ser usada com ferramentas de IA;  
* O arquivo `README.md` explica como instalar e executar o projeto.

Essa organização facilita a manutenção, a leitura e o reaproveitamento. A ideia é que uma pessoa do time consiga adicionar um novo dataset no futuro e rodar a análise sem precisar alterar o código.

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

## **Como a solução funciona? (Na prática)**

O fluxo da solução é simples. A pessoa informa o arquivo CSV que deseja analisar.

Por exemplo:

python src/analyze\_ab\_test.py \--file data/dataset\_01\_parceiroA.csv \--test-name "Teste Cashback Parceiro A"

A partir disso, o script executa as seguintes etapas:

1. Lê o arquivo CSV.  
2. Valida se as colunas necessárias existem.  
3. Converte datas.  
4. Converte valores monetários.  
5. Calcula métricas financeiras.  
6. Agrupa os dados por variante.  
7. Compara os grupos.  
8. Estima a consistência do resultado usando bootstrap.  
9. Gera relatório.  
10. Atualiza o tracker CSV.

Esse fluxo permite que os três datasets sejam processados sem alteração no código. Basta trocar o caminho do arquivo. Essa escolha foi importante porque o teste pedia uma solução reutilizável, não uma análise manual específica para cada parceiro.

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

## **Por que tratei os dados antes da análise?**

Antes de analisar qualquer resultado, tratei os dados. Essa etapa foi essencial porque os valores financeiros estavam em formato de moeda, como `R$ 10.000`.

Para uma pessoa, esse valor é fácil de entender. Mas para o código, ele pode ser interpretado como texto. Se eu tentasse calcular direto, poderia gerar erro ou resultado incorreto. Então, a solução transforma valores monetários em números.

Também normalizei nomes de colunas. Por exemplo, a coluna `Grupos de usuários` foi padronizada para `grupo`. Isso evita problemas com acentos, espaços e variações no nome das colunas. Essa preocupação torna a solução mais robusta para dados reais, onde pequenos problemas de formatação são comuns.

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

## **Qual foi a principal métrica escolhida?**

A métrica principal escolhida foi o lucro bruto médio diário. Calculei o lucro bruto assim:

lucro bruto \= comissão \- cashback

Essa métrica foi escolhida porque representa o resultado financeiro direto da operação.A comissão é o valor recebido pelo Méliuz. O cashback é o valor devolvido ao usuário. A diferença entre esses dois valores mostra quanto sobra antes de outros custos. Também usei a média diária para comparar os grupos de forma mais justa ao longo do período analisado.

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

## **Por que não escolhi só GMV como a métrica principal?**

GMV representa o volume total de vendas. Ele é importante, mas não pode ser analisado sozinho. Um grupo pode ter GMV maior porque ofereceu cashback maior. Porém, se o custo desse cashback for alto demais, o resultado final pode ser pior. Por exemplo:

* Grupo A vende R$ 1.000.000 e gera R$ 70.000 de lucro.  
* Grupo B vende R$ 1.200.000, mas gera R$ 40.000 de lucro.

Apesar do Grupo B vender mais, o Grupo A é melhor financeiramente. Por isso, usei GMV como métrica complementar, não como critério principal de decisão.

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

## **Por que não escolhi só compradores como a métrica principal?**

A quantidade de compradores também é importante, mas não conta a história inteira. Mais compradores podem significar mais crescimento. Porém, se esses compradores vieram apenas por causa de um incentivo caro demais, a campanha pode não ser sustentável. Por isso, avaliei compradores junto com lucro, margem e cashback distribuído. A decisão precisa considerar volume e eficiência ao mesmo tempo.

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

## **As outras métricas utilizadas**

Além do lucro bruto, utilizei outras métricas para enriquecer a análise. A margem sobre GMV mostra a eficiência financeira da variante. O cashback rate mostra quanto das vendas foi devolvido aos usuários como cashback. O lucro por comprador mostra quanto cada comprador gerou de resultado econômico. O ticket médio ajuda a entender o valor médio das compras. Essas métricas ajudam a evitar uma decisão baseada em apenas um número.

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

## **O uso do bootstrap**

Além das métricas consolidadas, usei bootstrap para estimar a probabilidade de cada grupo ser o melhor. Bootstrap é uma técnica estatística que simula vários cenários possíveis com base nos dados existentes. Na prática, a solução sorteia várias combinações dos dias analisados, calcula novamente o lucro médio de cada grupo e verifica qual grupo vence mais vezes. Isso ajuda a entender se o grupo vencedor parece consistente ou se venceu por pouca diferença. Usei essa técnica porque ela adiciona uma camada de confiança à recomendação.

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

## **Como o critério de decisão foi estruturado?**

Primeiro, identificar o grupo com maior lucro bruto médio diário.

Depois, verificar se esse grupo também preserva margem.

Em seguida, analisar se o resultado é consistente no bootstrap.

Por fim, avaliar se faz sentido escalar, manter o controle ou repetir o teste.

Esse critério evita decisões precipitadas. Se uma variante vende mais, mas perde margem, ela não deve ser escalada automaticamente. Se uma variante tem melhor resultado financeiro e boa consistência, ela se torna uma candidata mais forte.

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

## **Resultado do Parceiro A**

No Parceiro A, o Grupo 1 apresentou o melhor resultado financeiro. Segue o resumo dos principais resultados:

* Grupo 1: lucro total de R$ 404.711,00, lucro médio diário de R$ 4.399,03 e margem de 7,11%.  
* Grupo 2: lucro total de R$ 357.519,00, lucro médio diário de R$ 3.886,08 e margem de 5,60%.  
* Grupo 3: lucro total de R$ 264.287,00, lucro médio diário de R$ 2.872,68 e margem de 4,40%.

A probabilidade estimada de o Grupo 1 ser a melhor variante foi de 93,98%. Minha decisão para o Parceiro A foi manter o Grupo 1 como padrão. Embora outros grupos possam ter apresentado maior volume, o Grupo 1 foi mais eficiente financeiramente. Ele preservou mais lucro e melhor margem.

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

## **Resultado do Parceiro B**

No Parceiro B, o Grupo 1 também foi o vencedor. Segue o resumo dos principais resultados:

* Grupo 1: lucro total de R$ 286.570,00, lucro médio diário de R$ 4.697,87 e margem de 7,00%.  
* Grupo 2: lucro total de R$ 143.157,00, lucro médio diário de R$ 2.346,84 e margem de 5,00%.  
* Grupo 3: lucro total de R$ 52.593,00, lucro médio diário de R$ 862,18 e margem de 2,00%.

A probabilidade estimada de o Grupo 1 ser a melhor variante foi de 100%. Nesse caso, a recomendação é ainda mais clara. O aumento de cashback não compensou financeiramente. As variantes alternativas reduziram bastante o resultado econômico. Minha decisão para o Parceiro B foi manter o Grupo 1\.

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

## **Resultado do Parceiro C**

No Parceiro C, o Grupo 1 também apresentou o melhor resultado. Segue o resumo dos principais resultados:

* Grupo 1: lucro total de R$ 34.769,00, lucro médio diário de R$ 772,64 e margem de 2,00%.  
* Grupo 2: lucro total de R$ 0,00, lucro médio diário de R$ 0,00 e margem de 0,00%.

A probabilidade estimada de o Grupo 1 ser a melhor variante foi de 100%. O ponto mais crítico aqui é que o Grupo 2 não gerou lucro bruto. Isso indica que o cashback consumiu toda a comissão gerada. Minha decisão para o Parceiro C foi manter o Grupo 1\.

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

## **Minha recomendação consolidada**

Manter o Grupo 1 como padrão e não escalar as variantes com cashback maior para 100% do tráfego.

Essa decisão se sustenta porque, nos três testes, o Grupo 1 apresentou melhor resultado financeiro. As variantes com cashback maior não demonstraram ganho suficiente para compensar a perda de margem. Portanto, a tática recomendada é preservar o cashback do Grupo 1 como estratégia padrão e evitar escalar incentivos mais agressivos sem evidência clara de retorno financeiro.

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

## **Por que é que a Méliuz deveria adotar essa tática?**

Porque ela protege a rentabilidade sem abandonar o crescimento. Em um negócio de cashback, é tentador aumentar incentivos para gerar mais compras. Porém, se a análise não considerar o custo do cashback, o time pode escalar uma variante que cresce em volume, mas reduz o resultado financeiro. A tática que proponho é tomar decisões de Growth com base em eficiência econômica. Isso significa olhar para:

* Crescimento;  
* Custo do incentivo;  
* Margem;  
* Lucro bruto;  
* Consistência do resultado.

Essa abordagem reduz o risco de decisões baseadas em métricas de vaidade, como apenas vendas totais ou quantidade de compradores. A decisão passa a ser orientada por impacto real no negócio.

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

## **Benefícios pro time de Growth**

A solução traz benefícios práticos para o time. O primeiro benefício é redução de tempo. Se uma análise manual leva de 2 a 4 horas, a automação permite gerar uma primeira leitura em poucos minutos.

O segundo benefício é padronização. Todos os testes passam a ser analisados com o mesmo critério, reduzindo variações entre analistas.

O terceiro benefício é rastreabilidade. Cada teste analisado é registrado em um tracker, permitindo acompanhar histórico de experimentos, decisões tomadas e resultados.

O quarto benefício é escalabilidade. A mesma solução pode ser usada para novos parceiros e novos testes, desde que sigam o mesmo schema de dados.

O quinto benefício é integração com IA. A solução pode ser acionada com apoio de ferramentas como ChatGPT, Claude, Cursor ou Gemini. Assim, uma pessoa do time pode pedir a análise em linguagem natural, mas os cálculos seguem regras estruturadas.

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

## **Por que essa solução é considerada AI-Native**

Porque ela foi pensada para ser usada com ferramentas modernas de IA, mas sem depender de respostas subjetivas da IA. A IA entra como camada de produtividade. Ela pode ajudar a:

* Acionar a análise;  
* Explicar o relatório;  
* Transformar números em resumo executivo;  
* Revisar a clareza da recomendação;  
* Apoiar a documentação.

Mas a decisão não fica baseada em “achismo” da IA. A base da decisão vem do script, das métricas e dos dados. Essa combinação é importante porque une velocidade com confiabilidade.

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

## **Quais as limitações que foram identificadas?**

Uma limitação importante dos datasets é que eles não possuem visitantes, sessões ou usuários expostos por variante. Por isso, não foi possível calcular taxa de conversão real. A taxa de conversão exigiria uma informação como: Compradores / Usuários expostos. Como temos apenas compradores, comissão, cashback e vendas totais, a análise ficou focada em desempenho financeiro agregado. Essa limitação não invalida a decisão, mas deve ser considerada em testes futuros.Para análises ainda mais completas, eu recomendaria incluir nos próximos datasets:

* Usuários expostos por grupo;  
* Sessões;  
* Cliques;  
* Taxa de conversão;  
* Novos usuários versus recorrentes;  
* Segmentação por canal;  
* Dados de retenção ou recompra.

Com essas informações, seria possível avaliar não apenas lucro imediato, mas também impacto em aquisição e comportamento futuro.

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

## **Quais as possíveis evoluções para esta solução?**

A solução entregue é uma primeira versão funcional. Como próximos passos, eu evoluiria em quatro frentes:  A primeira seria integrar diretamente com Google Sheets, para registrar automaticamente os testes em uma planilha compartilhada.

A segunda seria gerar gráficos automaticamente em formato visual, facilitando apresentações para gestores.

A terceira seria criar um painel simples com histórico de testes, decisões e impacto financeiro.

A quarta seria transformar o fluxo em um agente de análise, onde a pessoa informa o arquivo e recebe automaticamente relatório, resumo executivo e recomendação.

Essas evoluções transformariam a solução em uma ferramenta interna cada vez mais completa para o time de Growth.

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

## **Conclusão**

Minha recomendação final é manter o Grupo 1 como padrão nos três parceiros analisados. A decisão não foi baseada apenas em maior volume de vendas, mas em eficiência financeira. Nos três casos, as variantes com cashback maior não compensaram a perda de margem. A tática que proponho é que a Méliuz adote uma régua de decisão para testes de cashback baseada em lucro bruto médio diário, margem e consistência do resultado. Essa abordagem ajuda o time a crescer com mais controle, reduzindo decisões inconsistentes e evitando escalar incentivos que aumentam custo sem gerar retorno proporcional. Além da recomendação específica para os três testes, a principal entrega é a solução reutilizável. Com ela, novos testes podem ser analisados rapidamente, com padronização, rastreabilidade e apoio de IA.

Em resumo, minha proposta é transformar uma análise manual e variável em um processo mais rápido, confiável e escalável para o time de Growth do Méliuz.

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

Agradeço pela oportunidade de participar deste desafio. Busquei construir uma solução prática, reutilizável e próxima de um cenário real do time de Growth, unindo análise de dados, visão de negócio e apoio de IA. Fico à disposição para explicar a solução, discutir melhorias e evoluir a proposta. Espero que curtam e que seja de utilidade para vocês, admiro muito a empresa e gostaria muito de fazer parte dela.

