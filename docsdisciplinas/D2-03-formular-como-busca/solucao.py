"""Lab 03 (caminho padrao): adaptacao do subproblema diagnostico ao dominio AMS.

A classe do catalogo e reaproveitada; apenas os dados do caso foram trocados.
"""

from __future__ import annotations

from comum.problemas.diagnostico import Diagnostico, Verificacao

CASO_AMS: tuple[Verificacao, ...] = (
    Verificacao("conferir delta de temperatura abaixo de 8,6 K (HDF)", 2.0, False, True),
    Verificacao("validar desgaste da ferramenta acima da faixa critica", 3.0, True, True),
    Verificacao("checar combinacao torque/rotacao em faixa extrema", 3.0, True, True),
    Verificacao("conferir ultima manutencao preventiva registrada", 4.0, False, False),
    Verificacao("verificar ocorrencias recentes da mesma maquina", 5.0, True, False),
    Verificacao("inspecionar alarmes operacionais da ultima hora", 6.0, False, False),
)

# Instancia alvo do verificador: python verificar-formulacao.py solucao.py:MEU_PROBLEMA
MEU_PROBLEMA = Diagnostico(CASO_AMS)
