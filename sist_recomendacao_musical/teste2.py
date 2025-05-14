from fastapi import FastAPI
from typing import List
from pydantic import BaseModel


app = FastAPI()


class Musica(BaseModel):
    id: int
    nome: str

class Error(BaseModel):
    message: str
    detail: str

class RespostaRecomendacao(BaseModel):
    recomendacoes: Musica

class RespostaError(BaseModel):
    error: Error


class RequisicaoRecomendacao(BaseModel):
    usuario_id: int = 123

    

@app.post(
    "/recomendar",
    response_model=RespostaRecomendacao,
    summary="Recomenda músicas para um usuário",
    description="Esse endpoint usa o sistema de recomendação para retornar músicas personalizadas para o usuário informado.",
    responses= {
        422: {
            "model": Error,
            "description": "Erro de validação. Os dados enviados não seguem o formato esperado.",
            "content": {
                "application/json": {
                    "example": {
                        "message": "Erro de validação",
                        "detail": "Campo 'usuario_id' deve ser um número inteiro."
                    }
                }
            },
        },
        404: {
            "model": Error,
            "description": "Usuário não encontrado.",
            "content": {
                "application/json": {
                    "example": {
                        "message": "Usuário não encontrado",
                        "detail": "Nenhum usuário com ID 999 foi encontrado."
                    }
                }
            },
        }
    }
)
def recomendar(req: RequisicaoRecomendacao):
    # Simulação de resposta
    return {
        "recomendacoes":
            {"id": 123, "nome": "Bohemian Rhapsody"}
    }