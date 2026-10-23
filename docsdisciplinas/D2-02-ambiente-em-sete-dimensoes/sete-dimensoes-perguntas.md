# Sete dimensões — perguntas para o meu ambiente

<!--
Este arquivo é o formulário do Laboratório 02: preencha DENTRO dele, na
seção do seu domínio, no fim. As perguntas por dimensão estão em comentário
como este — aparecem no editor, não na pré-visualização.

Em cada dimensão, a resposta tem duas partes obrigatórias: a classificação
e UMA FRASE de justificativa. A justificativa é o que a rubrica pontua — a
etiqueta sozinha não vale nada (slide 32). Quando a resposta honesta for
"depende", escreva de que depende e em que situação cada resposta se
aplica: isso é caracterização melhor, não pior.

Copie a tabela preenchida para a seção 2 do seu agent-spec.md ao terminar.
-->

## As sete perguntas (as mesmas do slide 22)

| Dimensão | A pergunta que ela faz |
|---|---|
| Observabilidade | O agente enxerga tudo o que precisa para decidir? |
| Número de agentes | Existe outro agente cujas ações afetam o resultado? |
| Determinismo | A mesma ação no mesmo estado dá sempre o mesmo efeito? |
| Episódico ou sequencial | A decisão de agora afeta as decisões seguintes? |
| Estático ou dinâmico | O ambiente muda enquanto o agente delibera? |
| Discreto ou contínuo | Estados e ações são contáveis ou variam sem degraus? |
| Conhecido ou desconhecido | O agente sabe de antemão as regras do ambiente? |

## O que prestar atenção em cada uma

- **Observabilidade** — o teste que decide: existe algo que muda a decisão
  correta e que o agente não mede? Se existe, é parcialmente observável,
  e o projeto precisa de estado interno. Quase todo domínio real é
  parcialmente observável; a resposta honesta aqui costuma ser "parcial".
- **Número de agentes** — um humano operador conta, se ele reage ao que o
  agente faz. Se a sua resposta for multiagente, a D11 será central para
  o seu projeto, e não periférica.
- **Determinismo** — é sobre o efeito das ações, não sobre a observação.
  E atenção: qualquer sistema que chame um modelo de linguagem tem uma
  ação estocástica no meio.
- **Episódico ou sequencial** — classificar um lote é episódico; conduzir
  um atendimento é sequencial. A consequência prática é o custo de
  avaliação: episódico avalia casos independentes, sequencial exige
  avaliar trajetórias inteiras.
- **Estático ou dinâmico** — dinâmico impõe prazo: resposta tardia é
  resposta errada. O caso do meio tem nome: semidinâmico, quando o
  ambiente não muda mas a nota do agente cai com a espera.
- **Discreto ou contínuo** — busca funciona sobre enumeração; contínuo
  precisa ser discretizado antes, e toda discretização perde informação.
  Se você discretizar, a granularidade é decisão declarada, com custo dos
  dois lados.
- **Conhecido ou desconhecido** — a distinção que mais confunde: trata do
  que o agente SABE sobre as regras, e não do que ele VÊ. Sistema legado
  sem documentação é ambiente desconhecido, mesmo que se enxergue tudo
  nele.

## As respostas do meu domínio

**Domínio:** AMS · Assistente de Manutenção Segura

| Dimensão | Minha classificação | Justificativa (uma frase) |
|---|---|---|
| Observabilidade | Parcialmente observável | O histórico de intervenções da máquina específica, a condição real da equipe e o texto das normas (ainda não lido) mudam a decisão correta, e o agente hoje só enxerga a leitura atual dos sensores e a descrição da ordem. |
| Número de agentes | Agente único | O escopo do agente é analisar a ordem, classificar o risco e enfileirar o parecer; o técnico e o supervisor agem depois, por um canal separado, sem contestar ou renegociar a classificação durante a avaliação. |
| Determinismo | Estocástico | A mesma leitura de sensores antecede falha em alguns casos e não em outros, e a chamada ao modelo de linguagem acrescenta variabilidade própria sobre a mesma entrada. |
| Episódico ou sequencial | Episódico | Cada ordem de serviço é avaliada isoladamente, em lote concorrente, sem o agente lembrar avaliações anteriores da mesma máquina. |
| Estático ou dinâmico | Semidinâmico | A máquina não muda radicalmente nos segundos da chamada ao modelo, mas o técnico tem pouco tempo entre ordens — uma resposta tardia perde valor mesmo sem o ambiente ter mudado. |
| Discreto ou contínuo | Contínuo | Temperatura, rotação, torque e desgaste são grandezas físicas reais e contínuas; é o agente que discretiza a saída em categorias fechadas (baixo/médio/alto, bloqueio sim/não), não o ambiente que nasce discreto. |
| Conhecido ou desconhecido | Desconhecido | Fora do limiar de HDF (8,6 K), os limiares dos demais modos de falha não estão documentados, e o corpus de normas (NR-10/12/35) ainda não é lido pelo agente — ele só conhece os nomes, não as regras. |

**O que a tabela de consequências obriga no meu projeto**:

- **Parcialmente observável → estado interno; memória e contexto.** Hoje o
  cliente processa cada ordem sem lembrar leituras anteriores da mesma
  máquina — precisa de um jeito de guardar e consultar esse histórico.
- **Agente único → sem protocolo de comunicação.** Ninguém disputa a
  classificação durante a avaliação: o técnico e o supervisor reagem depois,
  fora do escopo do agente (que só analisa, classifica e enfileira) — não é
  preciso prever nem negociar a reação deles dentro do ciclo de decisão.
- **Estocástico → valor esperado, nova tentativa, tempo máximo.** O `llm.py`
  já tem novas tentativas e tempo máximo de espera; falta tratar a incerteza
  do próprio nível de risco como probabilidade, não só como rótulo único.
- **Episódico → NÃO precisa de planejamento nem avaliação de trajetória
  inteira.** Isso economiza complexidade: basta avaliar um conjunto de
  ordens independentes, como o cliente já faz em lote.
- **Semidinâmico → prazo de resposta e resposta parcial aceitável.** Falta
  definir um limite de latência explícito e o que o sistema devolve se o
  modelo demorar além dele.
- **Contínuo → discretização declarada, com granularidade justificada.** A
  escolha de três níveis (baixo/médio/alto) em vez de uma escala contínua de
  risco precisa ser justificada, não assumida.
- **Desconhecido → fase de exploração e registro do que se aprendeu.** Ler o corpus
  normativo e registrar os limiares de cada modo de falha antes de confiar
  neles.
