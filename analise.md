# Análise — AMS (Assistente de Manutenção Segura)

## O que torna o problema difícil

Duas propriedades do ambiente (seção 2 do `agent-spec.md`) explicam a maior
parte dos 11 erros do baseline sobre os 30 casos do meu dataset
(`relatorio-de-desempenho.md`). A primeira é a **observabilidade parcial**:
o baseline decide só com a leitura do instante (vibração, temperatura) e
uma contagem de falhas recentes da família da máquina — ele não usa
`idade_meses` nem `horas_desde_manutencao`, mesmo esses campos estando no
próprio CSV. É exatamente aí que ele erra os casos M17, M18, M19 e M21:
vibração e temperatura ficam dentro do limiar reativo, a falha acontece
mesmo assim, e o agente conclui `seguir_operando` por não enxergar o sinal
que diferenciaria esse caso dos 16 que realmente não falham. A segunda é o
**determinismo estocástico**: a mesma combinação de leituras antecede
falha em alguns casos e não em outros (os 16 casos `seguir_operando` e os
14 de falha real não se separam por um único limiar linear), o que faz
qualquer regra reativa fixa — por melhor que seja o limiar escolhido —
acertar uma faixa e errar outra por construção, não por bug. Os 5 casos
M24, M26, M27, M29 e M30 (subescalonados de `parar_para_manutencao` para
`inspecionar_antes_de_operar`) mostram a mesma limitação num grau menor: o
baseline reconhece que há risco, mas não tem o segundo sinal que
distinguiria "inspecionar" de "parar".

## Que tipo de agente o problema realmente exige

Um reativo simples já está descartado — a observabilidade parcial obriga
estado interno, e o próprio baseline já é, tecnicamente, um reativo com
memória (`EstadoDaFrota` conta falhas recentes por janela de 7 dias). O que
a medição mostra é que memória sozinha não basta: `recallFalha = 0,7143`
fica abaixo do limiar de `0,90` porque a política usa só 2 das 6 colunas
disponíveis no caso. O problema pede um **agente baseado em utilidade**
(seção 3 do `agent-spec.md`), e a razão aparece direto na própria fórmula
de desempenho: ela não testa um objetivo binário, ela pondera
`recallFalha` contra `custoBloqueioIndevido` com um peso que penaliza o
custo em dobro. O exemplo numérico da seção 5 do `agent-spec.md` mostra por
que isso importa na prática — relaxar o limiar de bloqueio para capturar
mais falhas reais (subir `recallFalha` para `0,90`) pioraria o desempenho
agregado de `0,4643` para `0,30`, porque o custo de bloqueios indevidos
sobe junto. A escolha certa não é mexer no limiar; é dar ao agente mais
sinal para decidir — que é o que a busca informada  também reforça: o A* 
com heurística admissível só economiza
nós (11 contra 27 do custo uniforme) porque a heurística carrega
informação extra sobre a distância ao objetivo, não porque muda a regra de
decisão em si.

## O que isto muda no projeto (fecho)

É preciso trazer pelo menos um sinal novo que hoje existe no dado mas
não é usado pela política: `idade_meses` e/ou `horas_desde_manutencao`
combinados com vibração/temperatura, em vez de um limiar isolado — é
provável que isso resolva os falsos negativos completos (M17–M21) sem
piorar o custo de bloqueio indevido. O baseline reativo é competitivo
exatamente onde o limiar separa bem as classes (16 dos 19 acertos são
`seguir_operando` corretos, sem ambiguidade de sinal) — e isso não é
fracasso: é o sinal de que o próximo agente só precisa ganhar nuance nos
casos de fronteira, não reconstruir a decisão do zero.
