# Anotações — Laboratório 02, a descida à mão

> O critério do slide 11: as quatro perguntas respondidas por escrito, com o
> número que sustenta cada resposta. Preencha a tabela rodando o esqueleto
> com as três taxas do slide 12 e copiando a última linha de cada execução.

## A última linha de cada taxa

| Taxa | Última linha da saída (perda, w, b) |
|---|---|
| 0,001 | passo  200 perda 22462.1 w 215.016 b -17.7381 |
| 0,1 | passo  200 perda 0.752176 w 300.008 b 4.91185 |
| 1,5 | passo  200 perda inf w -3.12216e+190 b 4.826e+189 |

## As quatro perguntas do slide 11

**1. A perda está caindo a cada passo, ou oscilando?**

R: Depende da taxa. Com 0,001 caiu em todos os 199 deltas (0 subidas, 199
descidas). Com 0,1 houve oscilação no começo e no meio (55 subidas e 140
descidas), mas a tendência global é de queda forte até estabilizar. Com
1,5 a perda só sobe (160 subidas antes de explodir para inf).

**2. Ela estabiliza, ou continua descendo até o fim?**

R: Com 0,1 estabiliza: na cauda dos últimos 20 passos a variação ficou
praticamente zero (5.55e-16), com perda final 0.752176. Com 0,001 continua
descendo até o fim (perda final 22462.1 e cauda ainda variando 6044.9),
então está devagar demais em 200 passos. Com 1,5 não estabiliza: diverge.

**3. Os pesos encontrados batem com os que geraram os dados?**

R: Só com taxa 0,1. Os pesos verdadeiros são w=300 e b=5; com taxa 0,1
chegou em w=300.008 e b=4.91185 (muito perto). Com 0,001 ficou longe
(w=215.016, b=-17.7381). Com 1,5 explodiu para magnitude gigantesca
(w=-3.12216e+190, b=4.826e+189).

**4. Se algo divergiu, qual foi o primeiro passo estranho?**

R: Na taxa 1,5 o primeiro valor não finito da perda apareceu no passo 161
(perda vira inf). Se estender para 350 passos, o primeiro nan aparece no
passo 326.
