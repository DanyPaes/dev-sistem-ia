from fastapi import APIRouter, Query, HTTPException
from typing import List
from controller.material_controller import listar_materiais, obter_material_por_id
from schema.material import MaterialSchema

router = APIRouter(
    prefix="/material",
    tags=["Materiais"],
    responses={404: {"description": "Material não encontrado"}}
)

def df_to_list_dict_com_listas(df):
    # Se tiver alguma coluna que precisa virar lista, faz aqui (como fizemos pros alunos)
    # No momento não parece necessário, mas mantém o padrão
    return df.to_dict(orient='records')

@router.get("/", summary="Listar materiais", description="Retorna a lista completa de materiais didáticos disponíveis.", response_model=List[MaterialSchema])
def listar_todos_os_materiais():
    """
    Retorna uma lista com todos os materiais cadastrados.

    **Exemplo de uso**:  
    GET /material
    """
    df = listar_materiais()
    return df_to_list_dict_com_listas(df)

@router.get("/buscar", summary="Buscar material por ID", description="Retorna os dados de um material específico pelo seu ID.", response_model=List[MaterialSchema])
def buscar_material_por_id(id: int = Query(..., description="ID do material a ser buscado")):
    """
    Retorna os dados de um material específico, informando seu `id`.

    **Exemplo de uso**:  
    GET /material/buscar?id=10
    """
    resultado = obter_material_por_id(id)
    if not resultado:
        raise HTTPException(status_code=404, detail="Material não encontrado")
    return resultado
