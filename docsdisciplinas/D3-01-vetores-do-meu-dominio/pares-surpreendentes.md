# Pares que surpreenderam — Laboratório 01

> O slide 19 do D3-E1 pede DOIS casos anotados: um par PRÓXIMO sem razão
> aparente e um par DISTANTE que deveria estar junto. Eles voltam na D7,
> quando a turma montar o próprio índice de recuperação — escreva aqui e
> guarde este arquivo no seu repositório.

## Um par PRÓXIMO sem razão aparente

- Índices do par: (68, 107)
- As duas frases:
  - primeira: A malha de controle de temperatura do forno está oscilando além da banda permitida.
  - segunda: A chaminé do forno precisa de inspeção de refratário após o último choque térmico.
- Cosseno medido: 0.8034
- Por que essa proximidade surpreendeu:

R: As frases compartilham a palavra "forno", mas descrevem fenômenos diferentes
(controle de processo versus integridade estrutural da chaminé). O embedding
aproximou muito por sobreposição lexical do contexto térmico, mesmo sem serem
o mesmo tipo de decisão operacional.

## Um par DISTANTE que deveria estar junto

- Índices do par: (3, 23)
- As duas frases:
  - primeira: A análise de óleo do redutor não detectou partículas metálicas em excesso.
  - segunda: Planeje a parada programada da linha dois para a primeira semana de dezembro.
- Cosseno medido: -0.1695
- Por que essa distância surpreendeu:

R: No fluxo real de manutenção, diagnóstico de condição do redutor e
planejamento de parada programada costumam caminhar juntos (o diagnóstico
alimenta a decisão de quando parar). Mesmo assim, o par apareceu distante,
sugerindo que o modelo privilegiou termos superficiais e não captou bem a
relação de causa/planejamento entre as sentenças.

## O que a comparação com NORMALIZAR = True mudou

- Alguma ordem mudou? De qual par:

R: Na rodada com `QUANTOS = 200`, a ordenação por cosseno se manteve nos
extremos (os mesmos pares continuaram no topo e na cauda). O que mudou foi a
escala da distância euclidiana: sem normalizar os valores ficaram maiores e
influenciados pelo comprimento dos vetores; com normalização, os valores
ficaram comprimidos na faixa aproximada de 0,21 a 1,56 e comparáveis entre si.

Referência da execução:
- sem normalização: `saida-q200.txt`
- com normalização: `saida-q200-normalizado.txt`
