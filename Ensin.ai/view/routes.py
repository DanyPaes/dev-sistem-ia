from fastapi import APIRouter
from view import alunos_router
from view import material_router
from view import interacao_router
from view import recomendacao_hibrido_router
from view import metrics_router


router = APIRouter()

router.include_router(alunos_router.router)
router.include_router(material_router.router)
router.include_router(interacao_router.router)
router.include_router(recomendacao_hibrido_router.router)
router.include_router(metrics_router.router)

