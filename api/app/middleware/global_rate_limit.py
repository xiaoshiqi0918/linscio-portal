"""
In-memory global IP rate limit: 60 requests/minute per IP.
Uses a sliding window counter stored in a thread-safe dict.
"""
import time
import threading
from collections import defaultdict

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse


class GlobalRateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, max_requests: int = 60, window_seconds: int = 60):
        super().__init__(app)
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self._buckets: dict[str, list[float]] = defaultdict(list)
        self._lock = threading.Lock()

    def _get_client_ip(self, request: Request) -> str:
        forwarded = request.headers.get("X-Forwarded-For")
        if forwarded:
            return forwarded.split(",")[0].strip()
        real_ip = request.headers.get("X-Real-IP")
        if real_ip:
            return real_ip
        return request.client.host if request.client else "unknown"

    async def dispatch(self, request: Request, call_next) -> Response:
        ip = self._get_client_ip(request)
        now = time.time()
        cutoff = now - self.window_seconds

        with self._lock:
            timestamps = self._buckets[ip]
            self._buckets[ip] = [t for t in timestamps if t > cutoff]
            if len(self._buckets[ip]) >= self.max_requests:
                return JSONResponse(
                    status_code=429,
                    content={"success": False, "detail": "请求过于频繁，请稍后再试"},
                )
            self._buckets[ip].append(now)

        return await call_next(request)
