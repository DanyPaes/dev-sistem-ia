from pydantic import BaseModel
from typing import Optional

class InteracaoSchema(BaseModel):
    id_interacao: int
    id_aluno: int
    id_material: int
    tipo_interacao: str       # nome do campo do CSV
    avaliacao: Optional[int] = None
    duracao_minutos: Optional[int] = None
    data: str                 # string ISO datetime
