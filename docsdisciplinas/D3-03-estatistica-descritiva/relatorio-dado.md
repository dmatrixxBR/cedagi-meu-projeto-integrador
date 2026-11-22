# O meu dado, com rigor — relatório do Laboratório 03

Conjunto: `/Users/danielbarbosamartins/projetos/cedagi-meu-projeto-integrador/data/amostra/ai4i2020.csv` · 200 linhas · 14 variáveis

Medidas geradas pelo `medidas.py`: desvio padrão amostral (ddof=1),
quartis por interpolação linear, extremos pela regra da amplitude
interquartil — fora de 1,5 × a caixa (slide 24). As medidas são do
programa; as decisões são SUAS. Preencha todos os blocos `R:` e
confira com `python teste.py`.

## Medidas por variável

| variável | tipo | n | faltantes | média | mediana | desvio | Q1 | Q3 | AIQ | mín | máx |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| UDI | numérica | 200 | 0 | 5027.1950 | 5014.5000 | 2837.9039 | 2779.7500 | 7459.5000 | 4679.7500 | 138.0000 | 9998.0000 |
| Product ID | categórica (200 valores; moda: L55664) | 200 | 0 | — | — | — | — | — | — | — | — |
| Type | categórica (3 valores; moda: L) | 200 | 0 | — | — | — | — | — | — | — | — |
| Air temperature [K] | numérica | 200 | 0 | 300.1115 | 300.2000 | 2.0807 | 298.3000 | 301.8000 | 3.5000 | 295.6000 | 304.2000 |
| Process temperature [K] | numérica | 200 | 0 | 310.0475 | 310.1000 | 1.5444 | 308.8000 | 311.1000 | 2.3000 | 306.1000 | 313.8000 |
| Rotational speed [rpm] | numérica | 200 | 0 | 1528.5300 | 1472.0000 | 201.5680 | 1410.5000 | 1611.5000 | 201.0000 | 1278.0000 | 2678.0000 |
| Torque [Nm] | numérica | 200 | 0 | 41.4785 | 43.1000 | 10.6072 | 33.4000 | 49.0500 | 15.6500 | 10.7000 | 66.7000 |
| Tool wear [min] | numérica | 200 | 0 | 112.7750 | 115.0000 | 66.3876 | 57.5000 | 171.5000 | 114.0000 | 0.0000 | 240.0000 |
| Machine failure | numérica | 200 | 0 | 0.0400 | 0.0000 | 0.1965 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 1.0000 |
| TWF | numérica | 200 | 0 | 0.0150 | 0.0000 | 0.1219 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 1.0000 |
| HDF | numérica | 200 | 0 | 0.0050 | 0.0000 | 0.0707 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 1.0000 |
| PWF | numérica | 200 | 0 | 0.0100 | 0.0000 | 0.0997 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 1.0000 |
| OSF | numérica | 200 | 0 | 0.0150 | 0.0000 | 0.1219 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 1.0000 |
| RNF | numérica | 200 | 0 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |

## Extremos marcados (fora de 1,5 × a caixa — slide 24)

### Extremos de `Rotational speed [rpm]` — 8 valor(es), limites [1109.0000; 1913.0000]

| linha | valor |
|---:|---:|
| 4 | 2678.0000 |
| 54 | 2355.0000 |
| 59 | 2025.0000 |
| 86 | 2009.0000 |
| 91 | 1927.0000 |
| 114 | 2370.0000 |
| 122 | 1931.0000 |
| 133 | 2595.0000 |

Decisão sobre ESTES extremos — manter ou remover, caso a caso,
com o motivo (slide 25: quem remove sem dizer, mente por omissão):

R: Manter os 8/8 casos. Todos os valores (1927 a 2678 rpm) são
plausíveis para regime de operação e podem representar condição de estresse
ou ajuste de processo, não erro de digitação. Como o objetivo do domínio é
predizer falha, remover esses pontos reduziria justamente exemplos raros de
alto risco mecânico.

### Extremos de `Machine failure` — 8 valor(es), limites [0.0000; 0.0000]

| linha | valor |
|---:|---:|
| 4 | 1.0000 |
| 9 | 1.0000 |
| 23 | 1.0000 |
| 77 | 1.0000 |
| 83 | 1.0000 |
| 89 | 1.0000 |
| 132 | 1.0000 |
| 168 | 1.0000 |

Decisão sobre ESTES extremos — manter ou remover, caso a caso,
com o motivo (slide 25: quem remove sem dizer, mente por omissão):

R: Manter os 8/8 casos. Aqui "extremo" aparece por desbalanceamento
(Q1=Q3=0), não por erro de medição. O valor 1 é o evento-alvo de falha,
portanto é informação crítica e não pode ser removida sem distorcer o
problema supervisionado.

### Extremos de `TWF` — 3 valor(es), limites [0.0000; 0.0000]

| linha | valor |
|---:|---:|
| 23 | 1.0000 |
| 83 | 1.0000 |
| 168 | 1.0000 |

Decisão sobre ESTES extremos — manter ou remover, caso a caso,
com o motivo (slide 25: quem remove sem dizer, mente por omissão):

R: Manter os 3/3 casos (TWF=1). São ocorrências legítimas de um modo de
falha raro. Como é variável de desfecho técnico, não há justificativa
estatística ou de qualidade de dado para excluir.

### Extremos de `HDF` — 1 valor(es), limites [0.0000; 0.0000]

| linha | valor |
|---:|---:|
| 89 | 1.0000 |

Decisão sobre ESTES extremos — manter ou remover, caso a caso,
com o motivo (slide 25: quem remove sem dizer, mente por omissão):

R: Manter 1/1 caso (HDF=1). É evento raro, porém possível e esperado no
domínio. A remoção apagaria evidência de um mecanismo de falha real.

### Extremos de `PWF` — 2 valor(es), limites [0.0000; 0.0000]

| linha | valor |
|---:|---:|
| 4 | 1.0000 |
| 77 | 1.0000 |

Decisão sobre ESTES extremos — manter ou remover, caso a caso,
com o motivo (slide 25: quem remove sem dizer, mente por omissão):

R: Manter os 2/2 casos (PWF=1). Esses registros são semanticamente
consistentes com a variável (indicador binário de falha) e necessários para
treinar o reconhecimento de padrões de potência.

### Extremos de `OSF` — 3 valor(es), limites [0.0000; 0.0000]

| linha | valor |
|---:|---:|
| 9 | 1.0000 |
| 77 | 1.0000 |
| 132 | 1.0000 |

Decisão sobre ESTES extremos — manter ou remover, caso a caso,
com o motivo (slide 25: quem remove sem dizer, mente por omissão):

R: Manter os 3/3 casos (OSF=1). Mesma lógica dos demais indicadores
binários: "extremo" aqui significa minoria de classe, não outlier inválido.
Excluir reduziria cobertura dos modos de falha.


## Faltantes (os três mecanismos do slide 26)

Nenhuma variável tem valores faltantes.

## As quatro perguntas do slide 29

**1. Média e mediana se separam em alguma variável? Em qual?**

R: Sim. A separação mais evidente está em `Rotational speed [rpm]`
(média 1528.53 vs mediana 1472.00), indicando cauda à direita por valores
altos. Também aparece em `Torque [Nm]` (41.48 vs 43.10), sugerindo assimetria
em direção oposta.

**2. Quantos extremos foram marcados, e quantos você decidiu manter?**

R: Foram marcados 25 extremos no total (8 de velocidade + 8 de
Machine failure + 3 TWF + 1 HDF + 2 PWF + 3 OSF). Decisão: manter 25/25,
com justificativa de plausibilidade física e preservação de eventos raros.

**3. Algum faltante parece do terceiro mecanismo?**

R: Não se aplica neste recorte: o relatório encontrou 0 células faltantes.
Sem faltantes observados, não há como atribuir mecanismo 1, 2 ou 3.

**4. O que a análise da D1 não tinha visto?**

R: A D1 mostrou o panorama geral; aqui ficou quantitativamente explícito que
os "extremos" se concentram em variáveis-alvo binárias por desbalanceamento
(Q1=Q3=0) e em uma cauda alta de rotação. Essa distinção evita tratar evento
raro de falha como "ruído" e apagar sinal importante.

## Comparação com a análise exploratória da D1

O que mudou de lá para cá — o que a análise de lá não tinha visto,
e o que estas decisões escritas mudam no conjunto que a D5 vai usar:

R: Em relação à D1, este laboratório forçou uma política explícita de
tratamento: não remover automaticamente valores fora de 1,5*AIQ quando eles
forem eventos de interesse do domínio. O conjunto para D5 permanece íntegro
(200 linhas), sem descarte de casos raros, e com decisão documentada para
auditoria/reprodutibilidade.
