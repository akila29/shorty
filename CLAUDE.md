# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Run the app
python main.py

# Install dependencies (using uv, preferred; or pip)
uv sync

# Add a dependency
uv add <package>
```

**Migrations (Alembic)** — run before starting the app on a fresh DB:
```bash
alembic upgrade head       # apply all pending migrations
alembic downgrade -1       # roll back one migration
alembic revision -m "desc" # create a new migration
alembic history            # show applied migrations
```

Python version is pinned to **3.11** (`.python-version`).

## Architecture

This is a high-throughput URL shortener. The full design is in `URL Shortener — Design Summary.md`; the key points:

**Write path**: ALB → Fargate task → auto-increment ID generator → base62-encode to 7-char short code → write `(short_code, long_url)` to Postgres.

**Read path**: ALB uses hash-based routing (short code → consistent Fargate task) → Redis cache-aside (~0.1 ms hit) → Postgres fallback (~10 ms miss) → HTTP redirect.

**Core design decisions:**
- Auto-increment integer IDs (not hashing) — collision-free by construction, base62-encoded to 7 chars (62⁷ = 3.5 trillion codes)
- Same long URL always maps to the same short code (dedup at write time)
- Hash-based load balancing routes identical short codes to the same Fargate task, maximizing in-process or Redis cache hit rates
- Stateless API servers on Fargate; Redis Cluster (replicated + sharded) for read scale; single Postgres primary for writes

**Scale targets**: 1,157 writes/sec (100M URLs/day), 11,600 reads/sec (1B redirects/day).

## Project status

Section 1 (core service) is complete: FastAPI app with `POST /shorten` and `GET /{short_code}`, base62 ID encoding, asyncpg connection pool, Redis cache-aside, and Alembic migrations. Schema is managed by Alembic — run `alembic upgrade head` before starting the app on a fresh database.
