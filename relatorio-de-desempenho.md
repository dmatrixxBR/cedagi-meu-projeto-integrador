# Relatório de desempenho da linha de base

**Projeto:** AMS · Assistente de Manutenção Segura · **Data:** 2026-10-30

## 1. A métrica primária

`recallFalha` — (ordens com falha real classificadas como risco médio ou
alto, isto é, decisão ≠ `seguir_operando`) ÷ (total de ordens com falha
real no lote). Vem direto da fórmula de desempenho da seção 1 do
`agent-spec.md`: `Desempenho = recallFalha − (pesoCusto · custoBloqueioIndevido)`.

A métrica que o `medir.py` do pacote D2-06 imprime por padrão —
`acerto_da_decisao` — é uma proxy mais simples (decisão igual ao rótulo,
sobre o total); as duas estão reconciliadas na seção 2 abaixo, a partir da
mesma saída do agente.

## 2. O valor

Saída de `python -m ams.baseline` sobre `casos-meu-dataset.csv`:

```
Metrica: acerto_da_decisao
Valor: 19/30 = 0.6333
Conjunto: docsdisciplinas/D2-06-agente-baseline/casos-meu-dataset.csv
Distribuicao: {'seguir_operando': 16, 'inspecionar_antes_de_operar': 7, 'parar_para_manutencao': 7}
Qtde erros: 11
```

Reconciliando com a métrica do PEAS (seção 1 do `agent-spec.md`), sobre os
mesmos 30 casos:

- **`recallFalha` = 10/14 = 0,7143** (14 ordens são falha real; 4 delas —
  M17, M18, M19, M21 — foram classificadas como `seguir_operando`, um
  falso negativo completo). Limiar de sucesso: `≥ 0,90` — **não atingido**.
- **`custoBloqueioIndevido` = 2/16 = 0,125** (M01, M02 — ordens sem falha
  real que receberam `parar_para_manutencao`).
- **Desempenho agregado** (`pesoCusto = 2`): `0,7143 − 2·0,125 = 0,4643`.

## 3. O conjunto

Arquivo: `docsdisciplinas/D2-06-agente-baseline/casos-meu-dataset.csv` — 30
casos derivados do dataset real AI4I2020 (`data/raw/ai4i2020.csv`), com
datas sintéticas de abril/2026 atribuídas na extração. Distribuição dos
rótulos: 16 `seguir_operando`, 7 `inspecionar_antes_de_operar`, 7
`parar_para_manutencao` (14 são falha real, `falhou_depois=1`).

O conjunto de reserva do pacote (`casos-de-reserva.csv`, 30 casos) também
foi medido ao longo do laboratório — `25/30 = 0,8333` em `acerto_da_decisao`
— e é o conjunto usado pela suíte oficial (`teste.py`, 10 testes). Uso o meu
próprio conjunto aqui porque é o que reflete o dataset real do projeto;
ambos ficam declarados para não esconder a diferença.

## 4. Onde o agente erra

Casos com erro (`casos-meu-dataset.csv`):

- M01: decidiu `parar_para_manutencao`, correto era `seguir_operando`
- M02: decidiu `parar_para_manutencao`, correto era `seguir_operando`
- M17: decidiu `seguir_operando`, correto era `inspecionar_antes_de_operar`
- M18: decidiu `seguir_operando`, correto era `inspecionar_antes_de_operar`
- M19: decidiu `seguir_operando`, correto era `inspecionar_antes_de_operar`
- M21: decidiu `seguir_operando`, correto era `inspecionar_antes_de_operar`
- M24: decidiu `inspecionar_antes_de_operar`, correto era `parar_para_manutencao`
- M26: decidiu `inspecionar_antes_de_operar`, correto era `parar_para_manutencao`
- M27: decidiu `inspecionar_antes_de_operar`, correto era `parar_para_manutencao`
- M29: decidiu `inspecionar_antes_de_operar`, correto era `parar_para_manutencao`
- M30: decidiu `inspecionar_antes_de_operar`, correto era `parar_para_manutencao`

Os 11 erros caem em dois padrões distintos, não um só. O primeiro (M01,
M02) é falso positivo de bloqueio: vibração/temperatura levemente acima do
limiar reativo dispararam `parar_para_manutencao` sem falha real —
`custoBloqueioIndevido` mede exatamente esse padrão. O segundo, maior (9
dos 11 erros), é falha real mal graduada: 4 casos (M17–M21) o baseline não
viu risco nenhum, e 5 casos (M24–M30) ele viu risco mas subestimou a
gravidade (`inspecionar` em vez de `parar`).

A hipótese para os dois padrões é a mesma: o baseline só enxerga o instante
(vibração, temperatura) e uma contagem de falhas recentes da família da
máquina — ele não enxerga `idade_meses` nem `horas_desde_manutencao`
isoladamente da regra de limiar fixo, que é exatamente onde os casos
M17–M30 se diferenciam dos M01–M16 sem cruzar o limiar reativo. É um erro
de sensor construído, não de regra mal escrita: a leitura que decidiria
certo existe no CSV, mas a política atual não a usa.

## 5. A tabela comparativa de busca (item 4 da N2)

Tabela completa dos laboratórios 04 e 05 (fonte:
`docsdisciplinas/D2-04-busca-nao-informada/respostaLab04-05.md`):

| Busca | Custo | Ações | Nós expandidos | Nós gerados | Prof. máx. | Segundos |
|---|---:|---:|---:|---:|---:|---:|
| largura | 8.0 | 3 | 38 | 96 | 3 | 0.0001 |
| custo_uniforme | 8.0 | 3 | 27 | 76 | 3 | 0.0001 |
| profundidade_limitada(limite=32) | 8.0 | 3 | 4 | 3 | 3 | 0.0 |
| aprofundamento_iterativo(limite=32) | 8.0 | 3 | 34 | 45 | 3 | 0.0001 |
| gulosa[admissivel] | 8.0 | 3 | 4 | 15 | 3 | 0.0001 |
| a_estrela[admissivel] | 8.0 | 3 | 11 | 33 | 3 | 0.0001 |
| gulosa[inadmissivel] | 14.0 | 4 | 5 | 18 | 4 | 0.0 |
| a_estrela[inadmissivel] | 8.0 | 3 | 4 | 15 | 3 | 0.0 |

**A pergunta do item 4:** sim — o A* com a heurística admissível manteve o
custo ótimo (8.0, igual ao custo uniforme) e expandiu menos nós (11 contra
27 do custo uniforme, uma economia de ~59%). Isso diz que a heurística
admissível guia a busca corretamente para o mesmo mínimo sem o
custo uniforme precisar varrer tanta alternativa equivalente — o espaço de
estados do meu problema (ordem das verificações do diagnóstico AMS) tem um
único custo ótimo claro (soma das 3 verificações essenciais), e a
heurística aproxima bem essa distância restante.

**Ressalva de contagem:** a `profundidade_limitada` aparece com só 4 nós
expandidos porque, no meu problema, a primeira alternativa que ela explora
já bate no limite/objetivo — isso é uma vantagem da instância, não da
estratégia em geral; outra ordem de verificações no mesmo domínio poderia
exigir backtracking e mudar essa contagem.
