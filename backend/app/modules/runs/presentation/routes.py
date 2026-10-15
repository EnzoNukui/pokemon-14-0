"""Aggregate the run, draft, and run-battle route groups."""

from fastapi import APIRouter

from app.modules.runs.presentation.battle_routes import router as battle_router
from app.modules.runs.presentation.draft_routes import router as draft_router
from app.modules.runs.presentation.run_routes import router as run_router

router = APIRouter()
router.include_router(run_router)
router.include_router(draft_router)
router.include_router(battle_router)
