from pydantic import BaseModel, Field

class RecomendacaoHibridaItemSchema(BaseModel):
    """
    Representa uma recomendação de material didático gerada pelo sistema híbrido.

    A recomendação combina scores baseados em filtragem colaborativa e conteúdo textual.
    """
    id_material: int = Field(..., description="Identificador único do material recomendado")
    titulo: str = Field(..., description="Título do material recomendado")
    score_final: float = Field(..., description="Pontuação final da recomendação, combinada e ponderada")
