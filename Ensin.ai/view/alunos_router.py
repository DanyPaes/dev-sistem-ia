# view/alunos_router.py
from fastapi import APIRouter, Query
from typing import List
from controller.aluno_controller import listar_alunos, obter_aluno_por_id
from schema.aluno import AlunoSchema

router = APIRouter(
    prefix="/aluno",
    tags=["Alunos"],
    responses={404: {"description": "Aluno não encontrado"}}
)

@router.get(
    "/",
    summary="Listar alunos",
    description="Retorna a lista completa de alunos disponíveis no sistema.",
    response_model=List[AlunoSchema]
)
def listar_todos_os_alunos():
    """
    Retorna uma lista com todos os alunos cadastrados.

    **Exemplo de uso**:  
    GET /aluno
    """
    return listar_alunos().to_dict(orient='records')


@router.get(
    "/buscar",
    summary="Buscar aluno por ID",
    description="Retorna os dados de um aluno específico pelo seu ID.",
    response_model=List[AlunoSchema]
)
def buscar_aluno_por_id(id: int = Query(..., description="ID do aluno a ser buscado")):
    """
    Retorna os dados de um aluno específico, informando seu `id`.

    **Exemplo de uso**:  
    GET /aluno/buscar?id=4
    """
    aluno = obter_aluno_por_id(id)
    if not aluno:
        return []
    return aluno
