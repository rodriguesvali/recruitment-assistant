from __future__ import annotations

import logging
import os
from contextlib import asynccontextmanager
from time import perf_counter
from uuid import uuid4

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.requests import Request

from app.api.routes import router
from app.logging_config import configure_logging, request_id_context

configure_logging()

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(
        "application.startup",
        extra={
            "app_name": "recruitment-assistant-backend",
            "app_env": os.getenv("APP_ENV", "development"),
            "log_level": os.getenv("LOG_LEVEL", "INFO").upper(),
            "crewai_tracing_enabled": os.getenv("CREWAI_TRACING_ENABLED", "true").lower()
            in {"1", "true", "yes", "on"},
        },
    )
    yield
    logger.info("application.shutdown", extra={"app_name": "recruitment-assistant-backend"})


def create_app() -> FastAPI:
    app = FastAPI(
        title="Recruitment Assistant Backend",
        description="FastAPI backend for the Recruitment Assistant Application Crew.",
        version="0.1.0",
        lifespan=lifespan,
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost:4200",
            "http://127.0.0.1:4200",
            "http://localhost:4300",
            "http://127.0.0.1:4300",
            "http://localhost:5173",
            "http://127.0.0.1:5173",
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.middleware("http")
    async def request_logging_middleware(request: Request, call_next):
        request_id = request.headers.get("x-request-id") or uuid4().hex
        token = request_id_context.set(request_id)
        started_at = perf_counter()
        path = request.url.path
        method = request.method
        client_host = request.client.host if request.client else None

        logger.info(
            "api.request.start",
            extra={
                "method": method,
                "path": path,
                "client_host": client_host,
            },
        )
        try:
            response = await call_next(request)
        except Exception:
            duration_ms = round((perf_counter() - started_at) * 1000, 2)
            logger.exception(
                "api.request.error",
                extra={
                    "method": method,
                    "path": path,
                    "client_host": client_host,
                    "duration_ms": duration_ms,
                },
            )
            raise
        else:
            duration_ms = round((perf_counter() - started_at) * 1000, 2)
            response.headers["x-request-id"] = request_id
            logger.info(
                "api.request.complete",
                extra={
                    "method": method,
                    "path": path,
                    "status_code": response.status_code,
                    "duration_ms": duration_ms,
                    "client_host": client_host,
                },
            )
            return response
        finally:
            request_id_context.reset(token)

    app.include_router(router)
    return app


app = create_app()
