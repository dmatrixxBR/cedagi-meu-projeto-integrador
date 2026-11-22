# Relatório — item 1 da AO1 (D3): conjunto de 60 casos e duas variantes

## 1) Conjunto de casos

Arquivo: `casos-ams-60.csv` (60 casos — os 30 de `docsdisciplinas/D2-06-agente-baseline/
casos-meu-dataset.csv` + 30 novos, gerados por `gerar_casos_60.py` a partir do AI4I2020 bruto,
seed `60`, metodologia documentada no cabeçalho do script).

Distribuição de `acao_correta`: 32 `seguir_operando`, 14 `inspecionar_antes_de_operar`,
14 `parar_para_manutencao` (28 casos de falha real, `falhou_depois=1`).

## 2) As duas variantes

- **Variante A** — baseline do D2-06 (`src/ams/baseline.py`), sem alteração.
- **Variante B** — Variante A + regra nova: `horas_desde_manutencao >= 400` →
  `inspecionar_antes_de_operar`, inserida antes da regra de estado interno. Motivação:
  `analise.md` já apontava `horas_desde_manutencao`/`idade_meses` como sinal não usado pelo
  baseline, responsável pelos falsos negativos M17–M23. Definição em `variantes.py`.

## 3) Medição (`ao1.py`)

```
Variante A: 34/60 = 0.5667
Variante B: 37/60 = 0.6167
Diferença (B - A): +5.00 pontos percentuais
```

Tabela pareada (0=errou, 1=acertou):

|            | B errou | B acertou |
|------------|---------|-----------|
| A errou    | 22      | 4         |
| A acertou  | 1       | 33        |

Arquivo gerado: `acertos.csv` (colunas `variante_a`, `variante_b`, 0/1, uma linha por caso, mesma
ordem de `casos-ams-60.csv`).

## 4) Leitura honesta

+5,00 pp é exatamente o tamanho considerado como indistinguível de acaso com 60
casos pareados (régua: 10–12 pp). A Variante B parece melhor (4 casos corrigidos contra 1 caso
piorado), mas essa etapa **não** testa significância .

