# O mapa do meu domínio — conferência (Laboratório 04)

Conjunto: manutencao · 384 dimensões antes da redução
Escolha registrada (slide 55): normalizado · semente da vizinhança: 20260901
Mapas: mapa-do-espaco.png (componentes principais à esquerda, vizinhança à direita) · pontos: mapa-pontos.csv

## Passo 4 — os três pares que você escolheu no mapa (slide 52)

| par | cosseno original | a vizinhança visual |
|---|---|---|
| (35, 36) | +0.9780 | confirma |
| (60, 77) | +0.1228 | NÃO confirma |
| (30, 31) | +0.9426 | confirma |

## As quatro perguntas do slide 53

1. Os dois métodos produzem os mesmos agrupamentos?
R: Produzem agrupamentos parecidos em nível macro (temas de manutenção se
organizam em blocos visíveis nos dois mapas), mas não idênticos ponto a
ponto. Evidência: no mapa de vizinhança surgiu um par visualmente próximo
que no espaço original tem cosseno baixo (60,77 = +0.1228).

2. Há grupo que só aparece em um deles?
R: Sim. No mapa de vizinhança (t-SNE) os grupos locais ficam mais
compactos e separados visualmente; no mapa por componentes principais os
mesmos temas aparecem mais espalhados em gradiente. Ou seja, a separação
de "ilhas" é mais forte na vizinhança.

3. Os vizinhos visuais confirmam no cosseno original?
R: Nem sempre. Dos 3 pares escolhidos, 2 confirmaram com cosseno alto
((35,36)=+0.9780 e (30,31)=+0.9426), mas 1 não confirmou
((60,77)=+0.1228). Taxa de confirmação no recorte: 2/3.

4. O que aconteceria com um vetor novo, fora do conjunto?
R: Em componentes principais ele é projetado por transformação fixa
imediata: para o vetor 105 tratado como novo, a projeção foi (-0.195,
0.242). Já no mapa de vizinhança não existe posição direta para ponto novo:
é preciso refazer o mapa inteiro com o novo ponto incluído.

## O caso em que o mapa enganou (critério do slide 52)

Par e o que a figura sugeria, e o que o cosseno original disse:

R: Caso de engano registrado: par (60,77). No mapa de vizinhança os dois
pontos aparecem próximos (sugestão de semelhança), mas a conferência no
espaço original deu cosseno +0.1228, valor baixo para considerar semântica
realmente próxima neste conjunto.
