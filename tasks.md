
**1. Core service**
- [ ] Scaffold FastAPI project with `uv` and `pyproject.toml`
- [ ] Implement ID generator — Postgres `BIGSERIAL` auto-increment
- [ ] Implement base62 encoder
- [ ] `POST /shorten` — accepts long URL, returns short code
- [ ] `GET /{short_code}` — Redis lookup → Postgres fallback → 301 redirect
- [ ] Same URL → same short code (lookup before insert)
- [ ] Input validation — reject malformed URLs
- [ ] Error handling — 404 for unknown short codes

**2. Database**
- [ ] Write Postgres schema (`urls` table: `id`, `short_code`, `long_url`, `created_at`)
- [ ] Index on `short_code`
- [ ] Index on `long_url` (for same-URL deduplication lookup)
- [ ] Write Alembic migrations

**3. Cache**
- [ ] Set up Redis client (e.g. `redis-py` async)
- [ ] Implement cache-aside pattern in redirect endpoint
- [ ] Set TTL on cached keys (e.g. 24h)

**4. Containerisation**
- [ ] Write `Dockerfile` for the FastAPI service
- [ ] Write `.dockerignore`
- [ ] Write `docker-compose.yml` for local dev (FastAPI + Postgres + Redis)
- [ ] Test full flow locally via Docker Compose

**5. Cloud infrastructure (AWS)**
- [ ] Create ECR repository, push Docker image
- [ ] Provision RDS Postgres instance
- [ ] Provision ElastiCache Redis cluster
- [ ] Create ECS cluster + Fargate task definition
- [ ] Create ECS service with desired task count + Auto Scaling policy
- [ ] Create Application Load Balancer, attach to ECS service
- [ ] Configure security groups (ALB → Fargate → RDS/ElastiCache only)
- [ ] Store DB credentials in AWS Secrets Manager, inject into Fargate via env

**6. Domain & subdomain**
- [ ] Point your domain's DNS to Route 53 (or use existing registrar)
- [ ] Create subdomain (e.g. `tiny.yourdomain.com`) as an A record → ALB
- [ ] Provision SSL certificate via AWS ACM
- [ ] Configure HTTPS listener on ALB, redirect HTTP → HTTPS

**7. Frontend (React)**
- [ ] Scaffold React app (Vite + TypeScript)
- [ ] Input field for long URL + submit button
- [ ] `POST /shorten` call on submit, display short URL
- [ ] Copy-to-clipboard button
- [ ] Error states (invalid URL, service down)
- [ ] Deploy FE to S3 + CloudFront (or Vercel/Netlify if you prefer simplicity)
- [ ] Point subdomain or path to FE (e.g. `tiny.yourdomain.com` serves FE, `tiny.yourdomain.com/api` proxies to ALB)

**8. Observability**
- [ ] Structured logging in FastAPI (`structlog` or stdlib `logging`)
- [ ] CloudWatch log group for Fargate tasks
- [ ] Basic CloudWatch alarm — ALB 5xx rate > threshold
- [ ] Health check endpoint `GET /health` for ALB target group

**9. Nice to have (if time permits)**
- [ ] Rate limiting on `POST /shorten` (per IP) — prevent abuse
- [ ] URL expiry — TTL column in Postgres, background job to purge
- [ ] Click analytics — increment a counter in Redis per short code
- [ ] Custom short codes — let user specify their own alias

That's roughly the right order of execution too — service → DB → cache → Docker → cloud → domain → FE → observability. Each block depends on the previous one being stable.
