from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.core.config import get_settings
from app.db.database import engine, Base
from app.middleware.cors import setup_cors
from app.routes import user
from app.core.exception_handlers import register_exception_handlers

settings = get_settings()

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield 

app = FastAPI(
    title="Project API",
    description="This is a REST API for a project.",
    version=f"{settings.API_VERSION}.0.0",
    docs_url="/",
    redoc_url="/redoc",
    lifespan=lifespan
)

setup_cors(app)
register_exception_handlers(app)
app.include_router(user.router, prefix=settings.api_prefix)


