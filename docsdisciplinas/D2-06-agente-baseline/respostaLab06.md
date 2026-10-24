# Resposta Lab 06 - Agente Baseline

## 1) Conjunto de casos usado

Arquivo: casos-meu-dataset.csv

Total de casos: 30

Distribuicao dos rotulos (acao_correta):
- seguir_operando: 16
- inspecionar_antes_de_operar: 7
- parar_para_manutencao: 7

## 2) Metrica primaria (PEAS)

Metrica: acerto da decisao (casos com decisao igual ao rotulo, sobre o total)

Valor medido: 19/30 = 0.6333

PY
Metrica: acerto_da_decisao
Valor Medido: 19/30 = 0.6333
Conjunto: docsdisciplinas/D2-06-agente-baseline/casos-meu-dataset.csv
Distribuicao: {'seguir_operando': 16, 'inspecionar_antes_de_operar': 7, 'parar_para_manutencao': 7}
Qtde erros: 11

## 3) Onde o baseline erra

Casos com erro:
- M01
- M02
- M17
- M18
- M19
- M21
- M24
- M26
- M27
- M29
- M30

## 4) Analise (duas frases)

O baseline superestima risco em parte dos casos rotulados como seguir_operando e subestima parte dos casos que deveriam ser inspecionados ou parados.

Esse padrao de erro acontece porque as regras fixas de limiar e contagem por janela funcionam bem em casos faceis, mas perdem nuance em cenarios limitrofes e atipicos do dataset real.

## 5) Criterio de aceite do laboratorio

Criterio: baseline.py roda sobre 30 casos e devolve a metrica primaria.

Status: atendido.

Evidencia de execucao no baseline final do projeto (src/ams/baseline.py):
- metrica: acerto_da_decisao
- valor: 19/30 = 0.6333
- conjunto: docsdisciplinas/D2-06-agente-baseline/casos-meu-dataset.csv


