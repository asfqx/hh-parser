from app.handlers.start import router as start_router
from aiogram import Router
from app.handlers.search_resumes import router as search_router

router = Router()
router.include_router(start_router)
router.include_router(search_router)
