from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.cache import close_cache, init_cache
from app.database import close_db, init_db
from app.routes import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    await init_cache()
    yield
    await close_cache()
    await close_db()


app = FastAPI(title="URL Shortener", lifespan=lifespan)
app.include_router(router)
