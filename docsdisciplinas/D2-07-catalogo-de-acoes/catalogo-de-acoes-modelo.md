# Catálogo de ações — modelo para preencher

<!--
Este arquivo é para preencher: uma linha por ação que o SEU agente vai
poder executar. As perguntas de cada coluna estão aqui em comentário.

As quatro perguntas que decidem se uma linha está boa:
  - Ação de ESCRITA também? As que alteram o mundo são as que exigem
    cuidado — e são justamente as que mais ficam de fora.
  - COMUNICAR é ação? Avisar, escalar, transferir, pedir confirmação:
    entram com entrada, saída e risco como as outras.
  - "É reversível?" pergunta se o efeito pode ser DESFEITO sem custo
    maior que o da própria ação.
  - O risco diz risco DE QUÊ — "baixo" não é descrição; "paga duas vezes
    uma nota que já estava paga" é.

Este catálogo é, literalmente, a lista de ferramentas que você vai
implementar em D10. Cada linha vira uma função com contrato.
-->

| Ação | Entrada | Saída | É reversível? | Risco se errar |
|---|---|---|---|---|
| Ler a ordem de serviço | Identificador da máquina (Product ID, tipo L/M/H) | Leituras de temperatura do ar/processo, rotação, torque, desgaste + descrição textual da intervenção | Sim — só lê | Campo ausente ou leitura truncada leva o parecer a se apoiar em base incompleta |
| Executar uma verificação de risco (delta de temperatura para HDF, desgaste crítico, torque/rotação em faixa extrema, manutenção preventiva, ocorrências recentes) | Leituras da ordem + verificações já feitas (`feitas`, `positivas`) | Resultado positivo/negativo da verificação + estado atualizado | Sim — só computa | Falso negativo numa verificação crítica (ex.: HDF) deixa passar o modo de falha; falso positivo infla o risco sem motivo |
| Consultar o catálogo de normas potencialmente aplicáveis | Descrição da intervenção planejada | Lista de normas (NR-10/NR-12/NR-35) possivelmente aplicáveis, só pelos nomes | Sim — só lê | Norma relevante ausente na lista deixa o técnico sem o alerta de exigência de segurança |
| Classificar o risco e redigir o parecer | Resultado das verificações essenciais + normas indicadas | Parecer de risco (baixo/médio/alto) com justificativa textual | Sim — é rascunho antes de registrar | Falso negativo (classificar baixo quando é alto) é o erro mais caro do domínio; falso positivo custa bloqueio indevido |
| **Recomendar bloqueio e etiquetagem (LOTO)** | Parecer classificado como risco médio/alto | Recomendação de bloqueio enviada ao técnico/supervisor | Parcialmente — a recomendação pode ser retificada, mas se o bloqueio físico já foi iniciado a parada de produção não se desfaz sem custo | Comunicação: recomendar bloqueio indevido para quem não precisa custa produção parada; deixar de recomendar quando necessário expõe o técnico a risco físico real |
| Registrar o parecer e a justificativa para auditoria | Parecer final + normas indicadas + recomendação de bloqueio | Registro no log de auditoria do supervisor | Não — corrigir exige novo registro de retificação; o registro original permanece | Escrita: registro incorreto compromete a rastreabilidade exigida numa inspeção futura |
| **Escalar para inspeção humana (abster-se de decidir)** | Leitura inconsistente ou confiança estimada abaixo do limiar | Ordem encaminhada à fila do supervisor, sem parecer automático | Sim — a escalada pode ser revista se chegar nova leitura | Comunicação: escalar demais gera fadiga no supervisor (fila ignorada); escalar de menos deixa um caso de alto risco sem checagem humana |

**Quem executa cada ação** (o agente sozinho? com confirmação humana? só
humano?): Ler a ordem, executar as verificações, consultar normas, classificar
o risco e registrar o parecer são feitos pelo agente sozinho. Recomendar o
bloqueio/LOTO é decisão do agente, mas a *execução física* do bloqueio é
sempre do técnico/supervisor — o agente só recomenda. Escalar é o próprio
agente que decide se abstém de dar parecer; a partir daí, a inspeção em si é
só humana.

**O que o agente JAMAIS executa sozinho:** executar fisicamente o bloqueio e a
etiquetagem (LOTO) da máquina. O agente recomenda a parada e registra a
justificativa, mas quem interrompe a operação é o técnico ou o supervisor —
exatamente como "Reiniciar o serviço" no catálogo A: o efeito (produção
parada) não se desfaz, por isso essa ação não pode nascer sem uma confirmação
humana no caminho.
