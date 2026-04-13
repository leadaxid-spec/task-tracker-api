from fastapi import FastAPI
from app.auth import router
import logging
from app.core.config import settings

def get_application() -> FastAPI:
    application = FastAPI(
        title=f'{settings.PROJECT_NAME} Development Mode' if settings.ENV == "dev" else settings.PROJECT_NAME,
        version=settings.VERSION,
        docs_url="/docs" if settings.ENV == "dev" else None,
        redoc_url="/redoc" if settings.ENV == "dev" else None,
        openapi_url="/openapi.json" if settings.ENV == "dev" else None,
    )
    application.include_router(router=router)
    return application

app = get_application()