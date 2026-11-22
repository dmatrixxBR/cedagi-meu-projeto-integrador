"""Variante A e Variante B do agente baseline do AMS, para a AO1 (D3).

Variante A = o baseline do D2-06, sem alteração (src/ams/baseline.decidir).

Variante B = o baseline + UMA regra nova (não cosmética): usa
`horas_desde_manutencao` como segundo sinal reativo, antes da regra de
estado interno. A análise do D2 (`analise.md`) já apontava esse como o
sinal não utilizado que explica os falsos negativos do baseline
(M17–M23: casos de falha com vibração/temperatura dentro do limiar, mas
há muito tempo sem manutenção). A regra nova:

    se horas_desde_manutencao >= 400 -> "inspecionar_antes_de_operar"

Isso muda comportamento de verdade (não é so mexer num limiar numérico
isolado da mesma regra): acrescenta uma fonte de sinal que a Variante A
nunca olha, movendo decisões de `seguir_operando` para `inspecionar` em
casos de manutenção muito atrasada — com o trade-off esperado de também
gerar algum falso positivo novo (ex.: M10, que tem 426h e é
seguir_operando de verdade).
"""

from __future__ import annotations

from ams.baseline import (
    FALHAS_PARA_INSPECAO,
    LIMITE_TEMPERATURA,
    LIMITE_VIBRACAO,
    EstadoDaFrota,
)
from ams.baseline import decidir as decidir_a

LIMITE_HORAS_SEM_MANUTENCAO = 400.0


def decidir_b(registro: dict, estado: EstadoDaFrota) -> str:
    """Variante B: regra reativa original + sinal novo de manutenção atrasada."""
    if (
        registro["vibracao_mm_s"] > LIMITE_VIBRACAO
        or registro["temperatura_c"] > LIMITE_TEMPERATURA
    ):
        return "parar_para_manutencao"
    if registro["horas_desde_manutencao"] >= LIMITE_HORAS_SEM_MANUTENCAO:
        return "inspecionar_antes_de_operar"
    if estado.falhas_recentes(registro["tipo_maquina"]) >= FALHAS_PARA_INSPECAO:
        return "inspecionar_antes_de_operar"
    return "seguir_operando"


VARIANTES = {
    "variante_a": decidir_a,
    "variante_b": decidir_b,
}
