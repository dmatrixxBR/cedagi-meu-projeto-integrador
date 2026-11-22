"""ao1.py — item 1 da AO1 (D3): roda as DUAS variantes sobre os MESMOS 60
casos e grava `acertos.csv` (uma linha por caso, uma coluna por variante,
0/1), além de `latencias.json` com os tempos de invocação (item 2.4).

Uso:  python ao1.py
"""

from __future__ import annotations

import csv
import json
import time
from pathlib import Path

from ams.baseline import EstadoDaFrota, carregar_casos
from variantes import VARIANTES

AQUI = Path(__file__).resolve().parent
CASOS = AQUI / "casos-ams-60.csv"
SAIDA_ACERTOS = AQUI / "acertos.csv"
SAIDA_LATENCIAS = AQUI / "latencias.json"

REPETICOES_LATENCIA = 30  # invocações extras por caso, só para medir tempo


def avaliar_variante(casos: list[dict], decidir) -> list[int]:
    """Roda uma variante em ordem cronológica, com o próprio estado da
    frota (cada variante acumula memória própria — não compartilham)."""
    estado = EstadoDaFrota()
    acertos = []
    for registro in casos:
        decisao = decidir(registro, estado)
        acertos.append(1 if decisao == registro["acao_correta"] else 0)
        estado.registrar_desfecho(registro)
    return acertos


def medir_latencias(casos: list[dict], decidir) -> list[float]:
    """Latência por invocação (segundos), com estado novo a cada rodada —
    a medição de tempo não deve ser afetada pela posição no estado."""
    tempos = []
    for _ in range(REPETICOES_LATENCIA):
        estado = EstadoDaFrota()
        for registro in casos:
            inicio = time.perf_counter()
            decidir(registro, estado)
            tempos.append(time.perf_counter() - inicio)
            estado.registrar_desfecho(registro)
    return tempos


def main() -> None:
    casos = carregar_casos(CASOS)

    resultados = {nome: avaliar_variante(casos, decidir)
                  for nome, decidir in VARIANTES.items()}

    with SAIDA_ACERTOS.open("w", encoding="utf-8", newline="") as arquivo:
        escritor = csv.writer(arquivo)
        escritor.writerow(list(VARIANTES.keys()))
        for linha in zip(*resultados.values()):
            escritor.writerow(linha)

    acuracias = {nome: sum(valores) / len(valores)
                 for nome, valores in resultados.items()}
    print(f"Gravado {SAIDA_ACERTOS} ({len(casos)} casos).")
    for nome, acuracia in acuracias.items():
        print(f"  {nome}: {sum(resultados[nome])}/{len(casos)} = {acuracia:.4f}")

    latencias = {nome: medir_latencias(casos, decidir)
                 for nome, decidir in VARIANTES.items()}
    with SAIDA_LATENCIAS.open("w", encoding="utf-8") as arquivo:
        json.dump(latencias, arquivo, indent=2)
    print(f"Gravado {SAIDA_LATENCIAS} "
          f"({REPETICOES_LATENCIA} repetições x {len(casos)} casos por variante).")


if __name__ == "__main__":
    main()
