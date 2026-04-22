from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import auth, tasks
from app.core.config import settings
from app.db.database import init_db


@asynccontextmanager
async def lifespan(_: FastAPI):
    init_db()
    yield


app = FastAPI(
    title=settings.project_name,
    version="1.0.0",
    description=(
        "A task management backend with JWT authentication, role-based access, "
        "and PostgreSQL persistence."
    ),
    lifespan=lifespan,
    swagger_ui_parameters={"defaultModelsExpandDepth": -1},
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix=settings.api_v1_prefix)
app.include_router(tasks.router, prefix=settings.api_v1_prefix)


@app.get(
    "/health",
    tags=["Health"],
    summary="Health check",
    responses={
        200: {
            "description": "Service health status",
            "content": {
                "application/json": {
                    "example": {"status": "OK"}
                }
            },
        }
    },
)
def health_check() -> dict[str, str]:
    return {"status": "OK"}


@app.get(
    "/",
    tags=["Health"],
    summary="API home",
    responses={
        200: {
            "description": "API status",
            "content": {
                "application/json": {
                    "example": {
                        "message": "Task Management API is running.",
                        "docs_url": "/docs",
                    }
                }
            },
        }
    },
)
def read_root() -> dict[str, str]:
    return {
        "message": f"{settings.project_name} is running.",
        "docs_url": "/docs",
    }
