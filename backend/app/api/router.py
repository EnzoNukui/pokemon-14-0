from fastapi import APIRouter

from app.api.routes.health import router as health_router
from app.modules.accounts.presentation.routes import router as accounts_router
from app.modules.championship.presentation.routes import router as champions_router
from app.modules.runs.presentation.routes import router as runs_router

api_router = APIRouter()
api_router.include_router(health_router)
api_router.include_router(accounts_router)
api_router.include_router(runs_router)
api_router.include_router(champions_router)
