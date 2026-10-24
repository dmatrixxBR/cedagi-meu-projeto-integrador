"""Baseline agent for D2-06 (rule-based).

Implements the baseline decision policy and metric computation over a
30-case labeled set.
"""

from __future__ import annotations

import csv
from collections import Counter
from dataclasses import dataclass
from datetime import date as _date
from pathlib import Path
from typing import Callable

# Thresholds used by the baseline rules.
LIMITE_VIBRACAO = 7.0
LIMITE_TEMPERATURA = 78.0
FALHAS_PARA_INSPECAO = 2
JANELA_DIAS = 7


@dataclass
class ErroDecisao:
    id_caso: str
    decidiu: str
    correta: str


class EstadoDaFrota:
    """Internal memory: failures by machine family within a time window."""

    def __init__(self, janela_dias: int = JANELA_DIAS) -> None:
        self._janela = janela_dias
        self._falhas: list[tuple[str, _date]] = []
        self._ultima_data: _date | None = None

    def falhas_recentes(self, familia: str) -> int:
        if self._ultima_data is None:
            return 0
        limite = self._ultima_data.toordinal() - self._janela
        return sum(
            1
            for familia_vista, dia in self._falhas
            if familia_vista == familia and dia.toordinal() >= limite
        )

    def registrar_desfecho(self, registro: dict) -> None:
        self._ultima_data = _date.fromisoformat(registro["data"])
        if int(registro.get("falhou_depois", 0)) == 1:
            self._falhas.append((registro["tipo_maquina"], self._ultima_data))


def decidir(registro: dict, estado: EstadoDaFrota) -> str:
    """Baseline decision policy (reactive rule + stateful rule)."""
    if (
        registro["vibracao_mm_s"] > LIMITE_VIBRACAO
        or registro["temperatura_c"] > LIMITE_TEMPERATURA
    ):
        return "parar_para_manutencao"
    if estado.falhas_recentes(registro["tipo_maquina"]) >= FALHAS_PARA_INSPECAO:
        return "inspecionar_antes_de_operar"
    return "seguir_operando"


def carregar_casos(caminho: str | Path) -> list[dict]:
    with Path(caminho).open(encoding="utf-8-sig", newline="") as arquivo:
        casos = list(csv.DictReader(arquivo))
    casos.sort(key=lambda registro: registro["data"])
    for registro in casos:
        registro["idade_meses"] = int(registro["idade_meses"])
        registro["temperatura_c"] = float(registro["temperatura_c"])
        registro["vibracao_mm_s"] = float(registro["vibracao_mm_s"])
        registro["horas_desde_manutencao"] = float(registro["horas_desde_manutencao"])
        registro["falhou_depois"] = int(registro["falhou_depois"])
    return casos


def medir_baseline(
    caminho: str | Path,
    decisor: Callable[[dict, EstadoDaFrota], str] = decidir,
    classe_estado: type[EstadoDaFrota] = EstadoDaFrota,
) -> dict:
    """Returns the primary metric (decision accuracy) over labeled cases."""
    casos = carregar_casos(caminho)
    estado = classe_estado()
    acertos = 0
    erros: list[ErroDecisao] = []

    for registro in casos:
        acao = decisor(registro, estado)
        correta = registro["acao_correta"]
        if acao == correta:
            acertos += 1
        else:
            erros.append(
                ErroDecisao(
                    id_caso=registro["id_caso"],
                    decidiu=acao,
                    correta=correta,
                )
            )
        estado.registrar_desfecho(registro)

    total = len(casos)
    valor = acertos / total if total else 0.0
    return {
        "metrica": "acerto_da_decisao",
        "valor": valor,
        "acertos": acertos,
        "total": total,
        "distribuicao": dict(Counter(registro["acao_correta"] for registro in casos)),
        "erros": [erro.__dict__ for erro in erros],
        "caminho": str(caminho),
    }


def caminho_reserva_padrao() -> Path:
    raiz_repo = Path(__file__).resolve().parents[2]
    return raiz_repo / "docsdisciplinas" / "D2-06-agente-baseline" / "casos-de-reserva.csv"


if __name__ == "__main__":
    resultado = medir_baseline(caminho_reserva_padrao())
    print(
        f"Metrica primária: {resultado['metrica']} | "
        f"Valor: {resultado['acertos']}/{resultado['total']} = {resultado['valor']:.4f}"
    )
    print(f"Conjunto: {resultado['caminho']} ({resultado['total']} casos)")
