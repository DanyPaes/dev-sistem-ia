from fastapi import FastAPI
from view.routes import router as api_router

app = FastAPI(
    title="API de Recomendação Educacional ENSIN-AI",
    description="Sistema inteligente de recomendação de materiais para alunos.",
    version="1.0.0"
)

app.include_router(api_router)
