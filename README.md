# 1. Problema de negócio
A Curry Company é uma empresa de tecnologia que criou um
aplicativo que conecta restaurantes, entregadores e pessoas.
Através desse aplicativo, é possível realizar o pedido de uma refeição,
em qualquer restaurante cadastrado, e recebê-lo no conforto da sua
casa por um entregador também cadastrado no aplicativo da Curry
Company.

A Curry Company possui um modelo de negócio chamado
Marketplace, sendo o intermediário do negócio entre
restaurantes, entregadores e pessoas compradoras. Para
acompanhar o crescimento desses negócios, o CEO gostaria de ver
as seguintes métricas de crescimento:

## Do lado da empresa:
1. Quantidade de pedidos por dia.
2. Quantidade de pedidos por semana.
3. Distribuição dos pedidos por tipo de tráfego.
4. Comparação do volume de pedidos por cidade e tipo de tráfego.
5. A quantidade de pedidos por entregador por semana.
6. A localização central de cada cidade por tipo de tráfego.

## Do lado do entregador:
1. A menor e maior idade dos entregadores.
2. A pior e a melhor condição de veículos.
3. A avaliação médida por entregador.
4. A avaliação média e o desvio padrão por tipo de tráfego.
5. A avaliação média e o desvio padrão por condições climáticas.
6. Os 10 entregadores mais rápidos por cidade.
7. Os 10 entregadores mais lentos por cidade.

## Do lado do restaurantes:
1. A quantidade de entregadores únicos.
2. A distância média dos restaurantes e dos locais de entrega.
3. O tempo médio e o desvio padrão de entrega por cidade.
4. O tempo médio e o desvio padrão de entrega por cidade e tipo de
pedido.
5. O tempo médio e o desvio padrão de entrega por cidade e tipo de
tráfego.
6. O tempo médio de entrega durantes os Festivais.

# 2. Premissas assumidas para a análise

1. A análise foi realizada com dados entre 11/02/2022 e 06/04/2022.
2. Marketplace foi o modelo de negócio assumido.
3. As 3 principais visões do negócio foram: Visão empresa, visão restaurante e visão entregadores.

# 3. Estratégia da solução
O painel estratégico foi desenvolvido utilizando as métricas que
refletem as 3 principais visões do modelo de negócio da empresa:

1. Visão da empresa
2. Visão dos restaurantes
3. Visão dos entregadores

# 4. Top 3 Insights de dados
1. A sazonalidade da quantidade de pedidos é diária, e oscila por volta de 10%.
2. O maior tempo médio de entrega é para cidades “Semi-urban”, enquanto a maior distancia de entrega são para cidades do tipo “Urban”.
3. As maiores variações na avaliação das entregas, acontecem durante o
clima ensolarado.

# 5. O produto final do projeto
Painel online, hospedado em um Cloud e disponível para acesso em
qualquer dispositivo conectado à internet.
O painel pode ser acessado através desse link: https://dagoberto-project-curry-company.streamlit.app/

# 6. Conclusão
O objetivo desse projeto é criar um conjunto de gráficos e/ou tabelas
que exibam essas métricas da melhor forma possível para o CEO.
Da visão da Empresa, podemos concluir que o número de pedidos
cresceu entre a semana 06 e a semana 13 do ano de 2022.

