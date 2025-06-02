from fastapi import APIRouter, Query
from typing import List

# Importa seu schema e função recomendadora
from schema.recomendacao_hibrido import RecomendacaoHibridaItemSchema
from controller.recomendar_hibrido_controller import recomendar_hibrido

router = APIRouter()

@router.get(
    "/recomendacao_hibrida/",
    response_model=List[RecomendacaoHibridaItemSchema],
    summary="Obter recomendações híbridas para um aluno",
    description=(
        "Retorna uma lista dos materiais mais recomendados para o aluno especificado, "
        "com base em um modelo híbrido que combina recomendação colaborativa e conteúdo."
    ),
)
def obter_recomendacoes_hibridas(
    id_aluno: int = Query(..., description="ID do aluno para quem a recomendação será gerada"),
    top_n: int = Query(5, ge=1, le=20, description="Número máximo de recomendações a retornar")
):
    """
    Endpoint para obter recomendações híbridas personalizadas.

    - `id_aluno`: identificador do aluno
    - `top_n`: número de recomendações desejadas (padrão 5)

    Retorna uma lista ordenada de materiais recomendados com seus scores finais.
    """
    df_recomendacoes = recomendar_hibrido(id_aluno, top_n)
    return df_recomendacoes.to_dict(orient="records")
