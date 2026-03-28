import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.core.config import get_settings
from app.services.scheduler import init_scheduler, shutdown_scheduler

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s - %(message)s")


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()
    if settings.is_production:
        init_scheduler()
        logger.info("Scheduler started")
    yield
    if settings.is_production:
        shutdown_scheduler()


app = FastAPI(
    title="LinScio Portal API",
    version="1.0.0",
    lifespan=lifespan,
)

settings = get_settings()

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list or ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.exception("Unhandled exception: %s", exc)
    return JSONResponse(status_code=500, content={"success": False, "error": "internal_error"})


# --- Register routers ---
from app.api.v1.auth import router as auth_router
from app.api.v1.license import router as license_router
from app.api.v1.update import router as update_router
from app.api.v1.download import router as download_router
from app.api.v1.device import router as device_router
from app.api.v1.account import router as account_router
from app.api.v1.admin import router as admin_router

app.include_router(auth_router)
app.include_router(license_router)
app.include_router(update_router)
app.include_router(download_router)
app.include_router(device_router)
app.include_router(account_router)
app.include_router(admin_router)


@app.get("/health")
async def health():
    return {"status": "ok"}
