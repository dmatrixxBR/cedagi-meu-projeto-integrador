"""Gera casos-ams-60.csv: os 30 casos do Lab 06 + 30 casos novos extraídos
do AI4I2020 bruto, no mesmo esquema de colunas.

Metodologia dos 30 casos novos (documentada aqui porque o script de origem
dos 30 primeiros não foi versionado):

  - Amostragem estratificada do `data/raw/ai4i2020.csv` (seed fixa = 60,
    reprodutível), mantendo a mesma proporção de rótulos dos 30 originais
    (16 seguir_operando : 7 inspecionar : 7 parar), porque a taxa de falha
    natural do AI4I2020 (~3,4%) é baixa demais para dar casos de falha
    suficientes a um conjunto de avaliação pareado.
  - Mapeamento de colunas (determinístico, a partir do UDI/leituras brutas):
      tipo_maquina         = Type (L->TORNO, M->COMPRESSOR, H->PRENSA)
      idade_meses           = 15 + (UDI mod 110)
      temperatura_c         = Process temperature [K] - 273,15  (1 casa)
      vibracao_mm_s         = Torque [Nm] / 8                   (1 casa)
      horas_desde_manutencao= Tool wear [min] * 1.8             (1 casa)
      falhou_depois         = Machine failure
  - Rótulo (acao_correta) dos casos de falha: severidade =
    vibracao_mm_s + (temperatura_c - 35); severidade >= 6 -> parar,
    senão -> inspecionar (mesmo critério qualitativo usado na rotulagem
    original: vibração/temperatura mais altas => intervenção mais urgente).
  - Datas: continuam a sequência dos 30 originais (2026-04-16 a 2026-04-30,
    2 casos por dia), ids M31..M60.
"""

from __future__ import annotations

import csv
from datetime import date, timedelta
from pathlib import Path

import pandas as pd

AQUI = Path(__file__).resolve().parent
RAIZ_REPO = AQUI.parents[1]
CASOS_ORIGINAIS = RAIZ_REPO / "docsdisciplinas" / "D2-06-agente-baseline" / "casos-meu-dataset.csv"
RAW = RAIZ_REPO / "data" / "raw" / "ai4i2020.csv"
SAIDA = AQUI / "casos-ams-60.csv"

SEED = 60
N_SEGUIR = 16
N_INSPECIONAR = 7
N_PARAR = 7

MAPA_TIPO = {"L": "TORNO", "M": "COMPRESSOR", "H": "PRENSA"}
COLUNAS = [
    "id_caso", "data", "tipo_maquina", "idade_meses", "temperatura_c",
    "vibracao_mm_s", "horas_desde_manutencao", "acao_correta", "falhou_depois",
]


def _linha(udi: int, row: pd.Series, id_caso: str, dia: date, acao: str) -> dict:
    temperatura_c = round(row["Process temperature [K]"] - 273.15, 1)
    vibracao = round(row["Torque [Nm]"] / 8, 1)
    return {
        "id_caso": id_caso,
        "data": dia.isoformat(),
        "tipo_maquina": MAPA_TIPO[row["Type"]],
        "idade_meses": 15 + (udi % 110),
        "temperatura_c": temperatura_c,
        "vibracao_mm_s": vibracao,
        "horas_desde_manutencao": round(row["Tool wear [min]"] * 1.8, 1),
        "acao_correta": acao,
        "falhou_depois": int(row["Machine failure"]),
    }


def gerar_30_novos() -> list[dict]:
    bruto = pd.read_csv(RAW)

    sem_falha = bruto[bruto["Machine failure"] == 0]
    com_falha = bruto[bruto["Machine failure"] == 1].copy()
    com_falha["severidade"] = (com_falha["Torque [Nm]"] / 8) + \
        (com_falha["Process temperature [K]"] - 273.15 - 35)

    amostra_seguir = sem_falha.sample(n=N_SEGUIR, random_state=SEED)
    # separa falhas em "mais severas" (parar) e "menos severas" (inspecionar)
    falhas_ordenadas = com_falha.sort_values("severidade", ascending=False)
    amostra_parar = falhas_ordenadas.head(40).sample(n=N_PARAR, random_state=SEED)
    restante = falhas_ordenadas.drop(amostra_parar.index)
    amostra_inspecionar = restante.tail(60).sample(n=N_INSPECIONAR, random_state=SEED)

    rotulo_por_indice = {}
    for idx in amostra_seguir.index:
        rotulo_por_indice[idx] = "seguir_operando"
    for idx in amostra_inspecionar.index:
        rotulo_por_indice[idx] = "inspecionar_antes_de_operar"
    for idx in amostra_parar.index:
        rotulo_por_indice[idx] = "parar_para_manutencao"

    linhas_brutas = pd.concat([amostra_seguir, amostra_inspecionar, amostra_parar])
    linhas_brutas = linhas_brutas.sample(frac=1, random_state=SEED)  # embaralha a ordem de sorteio

    dia_inicial = date(2026, 4, 16)
    novos = []
    for posicao, (idx, row) in enumerate(linhas_brutas.iterrows()):
        dia = dia_inicial + timedelta(days=posicao // 2)
        id_caso = f"M{31 + posicao}"
        novos.append(_linha(row["UDI"], row, id_caso, dia, rotulo_por_indice[idx]))
    novos.sort(key=lambda linha: linha["data"])
    return novos


def main() -> None:
    with CASOS_ORIGINAIS.open(encoding="utf-8-sig", newline="") as arquivo:
        originais = list(csv.DictReader(arquivo))

    novos = gerar_30_novos()

    with SAIDA.open("w", encoding="utf-8", newline="") as arquivo:
        escritor = csv.DictWriter(arquivo, fieldnames=COLUNAS)
        escritor.writeheader()
        escritor.writerows(originais)
        escritor.writerows(novos)

    print(f"Gravado {SAIDA} com {len(originais) + len(novos)} casos "
          f"({len(originais)} originais + {len(novos)} novos).")


if __name__ == "__main__":
    main()
