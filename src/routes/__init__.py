from fastapi import APIRouter

from src.routes.cats.routes import router as cats_router
from src.routes.missions.routes import router as missions_router
from src.routes.targets.routes import router as targets_router

router = APIRouter(prefix="/api/v1")
router.include_router(cats_router)
router.include_router(missions_router)
router.include_router(targets_router)

__all__ = ["router"]
