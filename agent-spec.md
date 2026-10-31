# agent-spec.md — modelo do meu agente

<!--
Este arquivo é para preencher, não para ler e devolver. As perguntas de cada
seção estão em comentário como este: elas não aparecem na pré-visualização,
aparecem no editor. Responda ABAIXO de cada seção, apagando nada delas.

As seções que ainda não foram vistas em aula ficam de pé, com a linha
"quando se preenche" dizendo o encontro em que isso acontece. O documento
cresce a cada laboratório — o de hoje é o primeiro.

Preencha com exemplos concretos do SEU domínio. Uma linha que funcionaria
para qualquer empresa é uma linha genérica — o exemplo do seu segmento
(agente-spec-exemplo.pdf, no mesmo pacote) mostra o contraste.
-->

**Domínio:**  AMS · Assistente de Manutenção Segura
**Autor(a):** Daniel Barbosa Martins · **Última revisão:** 2026-10-30

---

## 1. PEAS

<!-- Perguntas que guiam o preenchimento:
  - Performance: o que conta como sucesso, em uma fórmula? Sobre o quê se
    conta, sobre qual conjunto, quanto é sucesso? Qual termo impede a
    trapaça mais óbvia (fechar rápido sem resolver)?
  - Environment: onde o agente opera? O que existe lá — sistemas, pessoas,
    documentos, ruído? Cite elementos concretos.
  - Actuators: o que o agente pode FAZER? Inclua comunicar e escalar:
    informar a decisão é uma ação, e passar adiante também é.
  - Sensors: o que o agente consegue PERCEBER? Só o que ele enxerga existe
    para ele.
  Um PEAS que menciona tecnologia de solução (banco vetorial, nome de modelo)
  está descrevendo a solução — o PEAS descreve o problema.
-->
**Quando se preenche:** no Laboratório 01, hoje. Refinado na Atividade Orientada.

**Performance:**

Medido sobre um lote de ordens de serviço com desfecho real conhecido (a
máquina falhou ou não, conforme o histórico/rótulo de manutenção):

`Desempenho = recallFalha −   (pesoCusto * custoBloqueioIndevido)`, onde:

- `recallFalha` = (ordens com falha real classificadas como risco médio ou
  alto) ÷ (total de ordens com falha real no lote);
- `custoBloqueioIndevido` = (ordens sem falha real em que o agente
  recomendou bloqueio/LOTO) ÷ (total de ordens sem falha real no lote);
- `pesoCusto` (ex.: 2) pesa o custo de parar a máquina sem necessidade frente ao
  custo de deixar passar uma falha real.

Sucesso: `recallFalha ≥ 0,90`. O termo que impede a trapaça —
responder sempre "risco baixo, sem bloqueio" para fechar rápido — é o
própio `recallFalha`: como a falha é rara (~3,4% das ordens), essa
estratégia dá `recallFalha = 0` e reprova de imediato, mesmo que a
acurácia geral pareça alta.

**Environment:**

O chão de fábrica e o fluxo de ordens de serviço de uma planta industrial:
máquinas identificadas por Product ID e tipo L/M/H, cada uma com sensores de
temperatura do ar e do processo, rotação, torque e desgaste da ferramenta;
uma ordem de serviço chega com a leitura atual e uma descrição livre da
intervenção planejada, escrita pelo técnico sob pressão de tempo. O corpus
normativo (NR-10, NR-12, NR-35 em PDF) existe como referência externa ao
ambiente operacional. O supervisor de segurança e o técnico agem depois do
parecer, por um canal separado (fila/log) — fora do escopo e do ciclo de
decisão do agente. Há ruído e imperfeição reais: leituras
podem ter o indicador geral de falha divergente dos cinco modos registrados, 
e o histórico de intervenções anteriores da máquina específica não está disponível no dado atual.

**Actuators:**

- Emitir um parecer de risco (baixo/médio/alto) com justificativa textual;
- indicar quais normas são potencialmente aplicáveis à intervenção descrita;
- recomendar (ou não) bloqueio e etiquetagem (LOTO) antes do início do serviço; 
- registrar o parecer e sua justificativa para auditoria posterior do supervisor; 
- escalar para inspeção humana — abster-se de decidir — quando a leitura for inconsistente 
  ou a confiança estimada for baixa demais para justificar uma recomendação.

**Sensors:**

- O identificador e o tipo da máquina (L/M/H); 
- a leitura atual dos sensores de temperatura do ar, temperatura do processo, rotação, 
    torque e desgaste da ferramenta; 
- a descrição textual da intervenção planejada, escrita pelo técnico na ordem de serviço. 

O agente **não** percebe o rótulo real de falha nem os cinco modos (isso é desfecho a ser previsto, não entrada);
não percebe o histórico de intervenções anteriores da máquina específica;
não percebe a condição real da equipe; e não lê o texto das
normas — só sabe seus nomes.

---

## 2. O ambiente em sete dimensões

<!--
Perguntas que guiam o preenchimento (uma por dimensão):
  - Observabilidade: existe algo que muda a decisão e o agente não mede?
  - Número de agentes: existe alguém cujas ações mudam o seu resultado?
    Um humano que reage ao agente conta.
  - Determinismo: a mesma ação no mesmo estado dá sempre o mesmo efeito?
  - Episódico ou sequencial: a decisão de agora afeta as decisões seguintes?
  - Estático ou dinâmico: o ambiente muda enquanto o agente delibera?
  - Discreto ou contínuo: estados e ações são contáveis?
  - Conhecido ou desconhecido: o agente sabe de antemão as regras? (Trata do
    que ele SABE, não do que ele VÊ.)
  Cada classificação vem com uma frase de justificativa — a etiqueta sozinha
  não vale nada.
-->
**Quando se preenche:** no Laboratório 02, no sábado (encontro 2).

| Dimensão | Minha classificação | Justificativa |
|---|---|---|
| Observabilidade | Parcialmente observável | O histórico de intervenções da máquina específica, a condição real da equipe e o texto das normas (ainda não lido) mudam a decisão correta, e o agente hoje só enxerga a leitura atual dos sensores e a descrição da ordem. |
| Número de agentes | Agente único | O escopo do agente é analisar a ordem, classificar o risco e enfileirar o parecer; o técnico e o supervisor agem depois, por um canal separado, sem contestar ou renegociar a classificação durante a avaliação. |
| Determinismo | Estocástico | A mesma leitura de sensores antecede falha em alguns casos e não em outros, e a chamada ao modelo de linguagem acrescenta variabilidade própria sobre a mesma entrada. |
| Episódico ou sequencial | Episódico | Cada ordem de serviço é avaliada isoladamente, em lote concorrente, sem o agente lembrar avaliações anteriores da mesma máquina. |
| Estático ou dinâmico | Semidinâmico | A máquina não muda radicalmente nos segundos da chamada ao modelo, mas o técnico tem pouco tempo entre ordens — uma resposta tardia perde valor mesmo sem o ambiente ter mudado. |
| Discreto ou contínuo | Contínuo | Temperatura, rotação, torque e desgaste são grandezas físicas reais e contínuas; é o agente que discretiza a saída em categorias fechadas (baixo/médio/alto, bloqueio sim/não), não o ambiente que nasce discreto. |
| Conhecido ou desconhecido | Desconhecido | Fora do limiar de HDF (8,6 K), os limiares dos demais modos de falha não estão documentados, e o corpus de normas (NR-10/12/35) ainda não é lido pelo agente — ele só conhece os nomes, não as regras. |

**O que a tabela de consequências obriga:** estado interno/memória
(observabilidade parcial), sem protocolo de comunicação a modelar (agente
único — técnico e supervisor reagem depois, fora do ciclo de decisão), valor
esperado com nova tentativa e tempo máximo (estocástico), discretização declarada da escala de risco
(contínuo), e uma fase de exploração do corpus normativo antes de confiar
nas regras (desconhecido). Por ser episódico, o projeto
**não** precisa de planejamento nem avaliação de trajetória inteira — só de
um conjunto de ordens independentes.

---

## 3. Tipo de agente pretendido

<!--
Perguntas que guiam o preenchimento:
  - O tipo mais simples que resolve: reativo simples, baseado em modelo,
    baseado em objetivos, baseado em utilidade, ou um deles com aprendizagem?
  - A caracterização do ambiente (seção 2) é que decide — parcialmente
    observável elimina o reativo simples.
  - Justifique com a dimensão do ambiente que obriga a escolha.
-->
**Quando se preenche:** no sábado (encontro 2, manhã).

**Agente baseado em utilidade, com estado interno (modelo do mundo).**

A observabilidade parcial já elimina o reativo simples: o
agente precisa lembrar as falhas recentes da família da máquina (é o que
`EstadoDaFrota` guarda no baseline) para decidir — a mesma leitura de
sensores, sem esse histórico, não basta. E o determinismo estocástico
sozinho já aponta para além de um agente baseado em metas: a fórmula de
desempenho da seção 1 não testa um objetivo binário ("resolveu/não
resolveu") — ela pondera dois termos que competem (`recallFalha` contra
`pesoCusto · custoBloqueioIndevido`). Comparar o valor esperado de decisões
conflitantes é exatamente o papel de uma função de utilidade, não de um
teste de objetivo.

**O que mudou e por quê (sem devolutiva do E3 até o momento):** não recebi
ainda a devolutiva do E3; esta seção foi preenchida agora, pela primeira
vez, com base direta na caracterização da seção 2 — não há mudança a
registrar porque não havia conteúdo anterior aqui.

---

## 4. Medida de desempenho

<!--
Perguntas que guiam o preenchimento:
  - A fórmula do campo Performance, agora em definição operacional: como se
    calcula, passo a passo, sem ambiguidade?
  - Métrica primária e duas secundárias. As secundárias pegam o que a
    primária deixa passar (custo, latência, reabertura).
  - O conjunto de casos: de onde vêm, quantos são, de que período.
  - O limiar de sucesso e o valor de hoje.
-->
**Quando se preenche:** a fórmula começa no Laboratório 01; a definição
operacional completa — primária, secundárias, conjunto e limiar — é item da
Atividade Orientada.

**Conjunto de casos:** `casos-meu-dataset.csv` (pacote `D2-06`) — 30 casos
derivados do dataset real AI4I2020 (`data/raw/ai4i2020.csv`), com datas
sintéticas de abril/2026 atribuídas na extração. Distribuição dos rótulos:
16 `seguir_operando`, 7 `inspecionar_antes_de_operar`, 7
`parar_para_manutencao` — 14 casos são falha real (`falhou_depois=1`).

**Métrica primária — `recallFalha`:** (falhas reais classificadas como
risco médio ou alto, ou seja, decisão ≠ `seguir_operando`) ÷ (total de
falhas reais no lote). Limiar de sucesso: `≥ 0,90` (seção 1). **Valor de
hoje: 10/14 = 0,7143 — abaixo do limiar.** O baseline erra 4 das 14
falhas reais por completo (M17, M18, M19, M21), classificando-as como
`seguir_operando`.

**Secundária 1 — `custoBloqueioIndevido`:** (ordens sem falha real em que
o agente recomendou `parar_para_manutencao`) ÷ (total de ordens sem falha
real). **Valor de hoje: 2/16 = 0,125** (casos M01, M02).

**Secundária 2 — taxa de subescalonamento:** (falhas reais que exigiam
`parar_para_manutencao` mas foram decididas como `inspecionar_antes_de_operar`)
÷ (total de falhas que exigiam parar). **Valor de hoje: 5/7 = 0,7143**
(M24, M26, M27, M29, M30) — a secundária que a primária sozinha não vê: o
baseline até reconhece risco nesses casos, só erra o grau.

**Desempenho agregado (fórmula da seção 1, `pesoCusto = 2`):**
`0,7143 − 2 · 0,125 = 0,4643`.

**O que mudou e por quê (sem devolutiva do E3 até o momento):** seção
preenchida agora pela primeira vez, com a medição real do Lab 06 sobre o
meu próprio conjunto de dados — não havia conteúdo anterior para comparar.

---

## 5. Restrições

<!--
Perguntas que guiam o preenchimento:
  - Latência aceitável: a partir de quantos segundos a resposta perde valor?
  - Custo aceitável: quanto pode custar cada resolução?
  - O que o agente jamais pode fazer: a ação irreversível que ele não executa
    sozinho. Esta linha vira política em D12.
  - A troca que você aceita: quanto de qualidade por quanto de custo?
    Um exemplo numérico vale mais que a fórmula.
-->
**Quando se preenche:** na Atividade Orientada.

*(O domínio — `dominio.md` — ainda não documenta um SLA formal de
latência/custo; os dois primeiros valores abaixo são premissas minhas,
assumidas explicitamente, até existir um número oficial do curso.)*

**Latência aceitável:** até 5 segundos por parecer. O técnico aguarda a
resposta na própria ordem de serviço antes de iniciar a intervenção — uma
resposta mais lenta que isso perde valor porque o trabalho fica parado no
chão de fábrica.

**Custo aceitável:** o custo da chamada ao modelo por ordem deve ficar bem
abaixo do custo de uma inspeção humana desnecessária — a ordem de grandeza
que guia o projeto, não um valor em R$ ainda medido.

**O que o agente jamais pode fazer sozinho:** executar fisicamente o
bloqueio e a etiquetagem (LOTO) da máquina (mesma restrição da seção 6) —
ele recomenda e registra, mas quem interrompe a operação é sempre o
técnico ou o supervisor.

**A troca que eu aceito (exemplo numérico):** subir `recallFalha` de 0,7143
para 0,90 relaxando o limiar de bloqueio deixaria `custoBloqueioIndevido`
subir de 0,125 para, digamos, 0,30. Com `pesoCusto = 2`, o desempenho
agregado cairia de `0,4643` (hoje) para `0,90 − 2·0,30 = 0,30` — pior do
que hoje. Ou seja: a fórmula já me impede de "comprar" recall só ficando
mais conservador; a melhoria real (D10) precisa vir de mais sinal (ex.:
histórico de manutenção), não de baixar a régua de bloqueio.

**O que mudou e por quê (sem devolutiva do E3 até o momento):** seção
preenchida agora pela primeira vez; os valores de latência/custo são
premissas explícitas, marcadas como tal, até haver um SLA documentado.

---

## 6. Catálogo de ações

<!--
Perguntas que guiam o preenchimento:
  - Para cada ação: nome, entrada, saída, é reversível?, qual o risco se
    errar? As quatro colunas são obrigatórias — "baixo" não é descrição de
    risco.
  - Ações de leitura E de escrita: as que alteram o mundo são as que exigem
    cuidado, e são justamente as que mais ficam de fora.
  - Este catálogo é, literalmente, a lista de ferramentas que você vai
    implementar em D10.
-->
**Quando se preenche:** na Atividade Orientada — o pacote `D2-07` traz o
modelo da tabela e dois exemplos preenchidos.

Catálogo completo (com os comentários de reversibilidade e risco) em
`docsdisciplinas/D2-07-catalogo-de-acoes/catalogo-de-acoes-modelo.md`.

| Ação | Entrada | Saída | É reversível? | Risco se errar |
|---|---|---|---|---|
| Ler a ordem de serviço | Identificador da máquina (Product ID, tipo L/M/H) | Leituras de temperatura do ar/processo, rotação, torque, desgaste + descrição textual da intervenção | Sim — só lê | Campo ausente ou leitura truncada leva o parecer a se apoiar em base incompleta |
| Executar uma verificação de risco (delta de temperatura para HDF, desgaste crítico, torque/rotação em faixa extrema, manutenção preventiva, ocorrências recentes) | Leituras da ordem + verificações já feitas (`feitas`, `positivas`) | Resultado positivo/negativo da verificação + estado atualizado | Sim — só computa | Falso negativo numa verificação crítica (ex.: HDF) deixa passar o modo de falha; falso positivo infla o risco sem motivo |
| Consultar o catálogo de normas potencialmente aplicáveis | Descrição da intervenção planejada | Lista de normas (NR-10/NR-12/NR-35) possivelmente aplicáveis, só pelos nomes | Sim — só lê | Norma relevante ausente na lista deixa o técnico sem o alerta de exigência de segurança |
| Classificar o risco e redigir o parecer | Resultado das verificações essenciais + normas indicadas | Parecer de risco (baixo/médio/alto) com justificativa textual | Sim — é rascunho antes de registrar | Falso negativo (classificar baixo quando é alto) é o erro mais caro do domínio; falso positivo custa bloqueio indevido |
| **Recomendar bloqueio e etiquetagem (LOTO)** | Parecer classificado como risco médio/alto | Recomendação de bloqueio enviada ao técnico/supervisor | Parcialmente — a recomendação pode ser retificada, mas se o bloqueio físico já foi iniciado a parada de produção não se desfaz sem custo | Comunicação: recomendar bloqueio indevido para quem não precisa custa produção parada; deixar de recomendar quando necessário expõe o técnico a risco físico real |
| Registrar o parecer e a justificativa para auditoria | Parecer final + normas indicadas + recomendação de bloqueio | Registro no log de auditoria do supervisor | Não — corrigir exige novo registro de retificação; o registro original permanece | Escrita: registro incorreto compromete a rastreabilidade exigida numa inspeção futura |
| **Escalar para inspeção humana (abster-se de decidir)** | Leitura inconsistente ou confiança estimada abaixo do limiar | Ordem encaminhada à fila do supervisor, sem parecer automático | Sim — a escalada pode ser revista se chegar nova leitura | Comunicação: escalar demais gera fadiga no supervisor (fila ignorada); escalar de menos deixa um caso de alto risco sem checagem humana |

**Quem executa cada ação:** ler, verificar, consultar normas, classificar e
registrar são do agente sozinho. Recomendar o bloqueio/LOTO é decisão do
agente, mas a execução física é sempre do técnico/supervisor. Escalar é o
agente que decide se abstém — a inspeção em si é só humana.

**O que o agente JAMAIS executa sozinho:** executar fisicamente o bloqueio e
a etiquetagem (LOTO) da máquina — o agente recomenda e registra, mas quem
interrompe a operação é sempre o técnico ou o supervisor.

---

## 7. Formulação por busca

<!--
Perguntas que guiam o preenchimento:
  - Qual fatia do problema é um espaço de estados? (Nem toda fatia é — e
    reconhecer a que não é vale tanto quanto formular a que é.)
  - Os cinco componentes: estado inicial, ações, modelo de transição, teste
    de objetivo, custo de caminho. Comece pelo teste de objetivo.
  - O estado descreve a SITUAÇÃO, não a história de como se chegou nela.
-->
— solucao.py:MEU_PROBLEMA
  1. estado é hashable ✅
  2. transição é função ✅
  3. ações estáveis na ordem ✅
  4. custo é positivo ou zero ✅
  5. objetivo é alcançável ✅
  6. estado não guarda o caminho ✅
  resumo: 6 ✅ · 0 ⚠️ · 0 ❌

**Quando se preenche:** no Laboratório 03, sábado à tarde (encontro 2).

 Subproblema escolhido (caminho padrão): **ordem das verificações do
diagnóstico de risco em uma ordem de serviço AMS**.

1. **Estado inicial**
  Situação sem verificação executada: `(feitas=(), positivas=())`.

2. **Ações**
  Executar uma verificação ainda não feita.
  Exemplos do caso AMS: conferir delta de temperatura para HDF, validar
  desgaste crítico, checar combinação torque/rotação em faixa extrema,
  conferir manutenção preventiva e ocorrências recentes.

3. **Transição (modelo de transição)**
  Ao executar uma ação `v`:
  - `v` entra no conjunto de `feitas`;
  - se o resultado da verificação no caso for positivo, `v` também entra em
    `positivas`.
  O estado é canônico (tuplas ordenadas), então duas trilhas diferentes para
  a mesma situação produzem o mesmo estado.

4. **Teste de objetivo**
  Objetivo alcançado quando todas as verificações essenciais do laudo foram
  realizadas (`essenciais ⊆ feitas`).

5. **Custo de caminho**
  Soma do tempo das verificações executadas (minutos).
  Custo de cada ação = tempo da verificação correspondente.

