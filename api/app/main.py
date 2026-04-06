import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.exception_handlers import (
    http_exception_handler,
    request_validation_exception_handler,
)
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.core.config import get_settings
from app.middleware.global_rate_limit import GlobalRateLimitMiddleware
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
    # 避免 /api/... 与 /api/.../ 的 301/302 重定向把 POST 变成 GET，导致注册/登录 405
    redirect_slashes=False,
)

settings = get_settings()

# 先加限流（靠内层）、后加 CORS（靠外层），使预检 OPTIONS 与跨域响应先经 CORS 处理
app.add_middleware(GlobalRateLimitMiddleware, max_requests=60, window_seconds=60)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list or ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    # 勿把框架自带的 4xx/422 当成未处理异常，否则可能被改成 500 或异常体格式错乱
    if isinstance(exc, (HTTPException, StarletteHTTPException)):
        return await http_exception_handler(request, exc)
    if isinstance(exc, RequestValidationError):
        return await request_validation_exception_handler(request, exc)
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
