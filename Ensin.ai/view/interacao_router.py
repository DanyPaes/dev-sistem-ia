from fastapi import APIRouter, Query, HTTPException
from typing import List
from controller.interacao_controller import listar_interacoes_por_aluno
from schema.interacao import InteracaoSchema

router = APIRouter(
    prefix="/interacoes",
    tags=["Interações"],
    responses={404: {"description": "Interações não encontradas"}}
)

@router.get("/", summary="Listar interações por aluno", description="Retorna a lista de interações realizadas por um aluno específico.", response_model=List[InteracaoSchema])
def listar_interacoes(id_aluno: int = Query(..., description="ID do aluno para listar as interações")):
    """
    Retorna todas as interações feitas por um aluno identificado pelo seu `id_aluno`.

    **Exemplo de uso**:  
    GET /interacoes?id_aluno=4
    """
    resultado = listar_interacoes_por_aluno(id_aluno)
    if not resultado:
        raise HTTPException(status_code=404, detail="Interações não encontradas para o aluno informado")
    return resultado
