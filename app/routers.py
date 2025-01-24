from fastapi import APIRouter
from app.services import login_service,registration_service,task_services,user_services,dashboard_service
router = APIRouter()
router.include_router(login_service.router)
router.include_router(registration_service.router)
router.include_router(task_services.router)
router.include_router(user_services.router)
router.include_router(dashboard_service.router)
