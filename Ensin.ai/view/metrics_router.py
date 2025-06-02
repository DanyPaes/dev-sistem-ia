from fastapi import APIRouter, Query
from typing import Union

from schema.metrics import MetricasOfflineSchema, MetricasOnlineSchema
from controller.metrics_controller import calcular_metricas_offline, calcular_metricas_online

router = APIRouter()

@router.get(
    "/metricas/offline/",
    response_model=MetricasOfflineSchema,
    summary="Calcular métricas offline para recomendação híbrida",
    description=(
        "Calcula métricas clássicas de avaliação offline (precisão, recall, f1, coverage, diversity) "
        "para as recomendações geradas para o aluno especificado."
    )
)
def obter_metricas_offline(
    id_aluno: int = Query(..., description="ID do aluno para o cálculo das métricas"),
    top_n: int = Query(5, ge=1, le=50, description="Número de recomendações a considerar no cálculo")
):
    """
    Endpoint para calcular métricas offline das recomendações híbridas.

    Parâmetros:
    - `id_aluno`: Identificador do aluno.
    - `top_n`: Número de itens recomendados para avaliar.

    Retorna as métricas de desempenho do sistema para esse aluno.
    """
    resultados = calcular_metricas_offline(id_aluno, top_n)
    return resultados


@router.get(
    "/metricas/online/",
    response_model=MetricasOnlineSchema,
    summary="Obter métricas online do sistema de recomendação",
    description="Retorna métricas online do sistema, atualmente com valores fixos (placeholders)."
)
def obter_metricas_online():
    """
    Endpoint para obter métricas online do sistema.

    Atualmente os valores são fixos como placeholders.
    """
    resultados = calcular_metricas_online()
    return resultados
