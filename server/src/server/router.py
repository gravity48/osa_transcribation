from server.base import DefaultRouter
from server.endpoints.database import db_router
from server.endpoints.project import project_router

router = DefaultRouter()

router.include_router(db_router)

router.include_router(project_router)
