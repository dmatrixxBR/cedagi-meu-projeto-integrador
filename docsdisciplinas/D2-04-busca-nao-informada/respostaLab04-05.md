solucao.py:MEU_PROBLEMA
  1. estado é hashable ✅
  2. transição é função ✅
  3. ações estáveis na ordem ✅
  4. custo é positivo ou zero ✅
  5. objetivo é alcançável ✅
  6. estado não guarda o caminho ✅
  resumo: 6 ✅ · 0 ⚠️ · 0 ❌

Seis verificações verdes — a formulação pode ir para o agent-spec.md e para o lab-04.
danielbarbosamartins@MacBook-Pro-de-Daniel D2-03-formular-como-busca %  cd /Users/danielbarbosamartins/projetos/cedagi-meu-projeto-integrador/docsdisciplinas/D2-04-busca-nao-informada && python esqueleto.py
Formulação: ../../docs/D2-03-formular-como-busca/solucao.py:MEU_PROBLEMA

| Busca                              | Custo | Ações | Nós expandidos | Nós gerados | Prof. máx. | Segundos |
|:-----------------------------------|------:|------:|---------------:|------------:|-----------:|---------:|
| largura                            |   8.0 |     3 |             38 |          96 |          3 |   0.0001 |
| custo_uniforme                     |   8.0 |     3 |             27 |          76 |          3 |   0.0001 |
| profundidade_limitada(limite=32)   |   8.0 |     3 |              4 |           3 |          3 |      0.0 |
| aprofundamento_iterativo(limite=32)|   8.0 |     3 |             34 |          45 |          3 |   0.0001 |
| gulosa[admissivel]                 |   8.0 |     3 |              4 |          15 |          3 |   0.0001 |
| a_estrela[admissivel]              |   8.0 |     3 |             11 |          33 |          3 |   0.0001 |
| gulosa[inadmissivel]               |  14.0 |     4 |              5 |          18 |          4 |      0.0 |
| a_estrela[inadmissivel]            |   8.0 |     3 |              4 |          15 |          3 |      0.0 |

Conclusão

Alguma busca achou caminho mais barato que a largura?
Não. O menor custo foi igual em todas as buscas: 8.0.

Análise do porquê
Meu problema tem 3 verificações essenciais com custos 2 + 3 + 3, e o objetivo exige completar as essenciais.
Como o custo do caminho ótimo é exatamente essa soma, as buscas acabam chegando ao mesmo custo mínimo.
O custo uniforme não melhorou o custo final, mas foi mais eficiente em exploração do que largura.
A profundidade limitada parece muito light em nós, mas isso é em parte definição de métrica: nela, a busca vai parar
na primeira alternativa, o que no cenário do meu problema, aparentemente tem vantagem deste método em contagem.

Justificativa das duas heurísticas

Lembrando o conceito de heurística, ela define um caminho das pedras para solucionar um problema, mas não 
significa que aquele caminho tomado, se aplica a todas as problemáticas possíveis, nem seria o melhor caminho.

Entre heurísticas admissíveis, domina a que estima sempre mais alto sem superestimar;
A heurística inadmissível não entra nesse critério porque perde a garantia do A*.

Na evidência desta instância, a heurística inadmissível guiou o A* com menos expansão (4 contra 11 da admissível),
mas esse ganho vem sem garantia geral e já mostrou risco na gulosa: custo 14.0 (pior que o ótimo 8.0).
Ou seja, ela pode parecer mais "agressiva" em expansão, mas é menos confiável em qualidade de solução.

Eu estabeleci o meu critério confiabilidade no diagnóstico, ou seja, achar o ótimo de forma garantida, então para mim a 
melhor heurística foi a admissível a_estrela, embora a gulosa admissível tenha tido mesmo custo e menor número de nós expandidos e gerados, nem sempre isso será realidade dependendo do cenário aplicado de verificações;