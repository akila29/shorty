from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import RedirectResponse
from asyncpg.exceptions import UniqueViolationError

from app.cache import cache_get, cache_set
from app.database import get_pool
from app.encoder import encode
from app.models import ShortenRequest, ShortenResponse

router = APIRouter()


@router.post("/shorten", response_model=ShortenResponse)
async def shorten(body: ShortenRequest, request: Request) -> ShortenResponse:
    long_url = str(body.url)
    pool = get_pool()

    async with pool.acquire() as conn:
        async with conn.transaction():
            row = await conn.fetchrow(
                "SELECT short_code FROM urls WHERE long_url = $1", long_url
            )
            if row:
                short_code = row["short_code"]
            else:
                try:
                    # Reserve the next ID from the sequence, compute short_code,
                    # then insert both in one round-trip — avoids the placeholder problem.
                    new_id = await conn.fetchval("SELECT nextval('urls_id_seq')")
                    short_code = encode(new_id)
                    await conn.execute(
                        "INSERT INTO urls (id, long_url, short_code) VALUES ($1, $2, $3)",
                        new_id,
                        long_url,
                        short_code,
                    )
                except UniqueViolationError:
                    row = await conn.fetchrow(
                        "SELECT short_code FROM urls WHERE long_url = $1", long_url
                    )
                    short_code = row["short_code"]

    short_url = str(request.base_url) + short_code
    return ShortenResponse(short_code=short_code, short_url=short_url, long_url=long_url)


@router.get("/{short_code}")
async def redirect(short_code: str) -> RedirectResponse:
    long_url = await cache_get(short_code)

    if not long_url:
        pool = get_pool()
        async with pool.acquire() as conn:
            row = await conn.fetchrow(
                "SELECT long_url FROM urls WHERE short_code = $1", short_code
            )
        if not row:
            raise HTTPException(status_code=404, detail="Short code not found")
        long_url = row["long_url"]
        await cache_set(short_code, long_url)

    return RedirectResponse(url=long_url, status_code=301)
