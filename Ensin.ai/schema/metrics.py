from pydantic import BaseModel, Field

class MetricasOfflineSchema(BaseModel):
    """
    Métricas de avaliação offline para o sistema de recomendação híbrida.
    """
    precisao: float = Field(..., description="Precisão das recomendações (precision)")
    recall: float = Field(..., description="Recall das recomendações")
    f1_score: float = Field(..., description="F1-score das recomendações")
    rmse: float = Field(..., description="Root Mean Squared Error (fixo, neste caso 0)")
    coverage: float = Field(..., description="Cobertura das recomendações (coverage)")
    diversity: float = Field(..., description="Diversidade das recomendações (diversity)")


class MetricasOnlineSchema(BaseModel):
    """
    Métricas de avaliação online para o sistema de recomendação.
    (valores fixos atualmente, placeholders)
    """
    ctr: int = Field(..., description="Click Through Rate (taxa de cliques)")
    pesquisa: int = Field(..., description="Número de pesquisas realizadas")
    engajamento: int = Field(..., description="Nível de engajamento do usuário")
