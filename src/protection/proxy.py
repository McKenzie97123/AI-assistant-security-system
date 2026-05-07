import os
import time
import logging
import httpx
import redis.asyncio as aioredis
from fastapi import FastAPI, Request
from fastapi.responses import Response, JSONResponse
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

from analyzer import RequestAnalyzer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

WEBAPP_URL = os.getenv("WEBAPP_URL", "http://webapp-svc:8080")
REDIS_URL = os.getenv("REDIS_URL", "redis://redis-svc:6379")

requests_total = Counter("proxy_requests_total", "Total requests", ["result"])
detection_latency = Histogram("proxy_detection_latency_seconds", "Detection latency")
blocks_by_method = Counter("proxy_blocked_by_method_total", "Blocks by detection method", ["method"])

app = FastAPI(title="AI Bot Protection Proxy")
analyzer: RequestAnalyzer | None = None


@app.on_event("startup")
async def startup():
    global analyzer
    redis = aioredis.from_url(REDIS_URL, decode_responses=True)
    analyzer = RequestAnalyzer(redis)
    logger.info(f"Protection proxy started — strategy={os.getenv('PROTECTION_STRATEGY', 'ml')}")


@app.get("/metrics")
async def metrics():
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)


@app.get("/health")
async def health():
    return {"status": "healthy", "timestamp": time.time()}


@app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def proxy(request: Request, path: str):
    body = await request.body()

    t0 = time.perf_counter()
    features = await analyzer.extract_features(request, body)
    result = await analyzer.analyze(features)
    detection_latency.observe(time.perf_counter() - t0)

    if result.blocked:
        requests_total.labels(result="blocked").inc()
        blocks_by_method.labels(method=result.method).inc()
        logger.info(f"BLOCKED {request.client.host} score={result.score:.2f} reason={result.reason}")
        return JSONResponse(
            status_code=429,
            content={"error": "Request blocked", "reason": result.reason},
        )

    requests_total.labels(result="allowed").inc()

    target = f"{WEBAPP_URL}/{path}"
    if request.url.query:
        target += f"?{request.url.query}"

    forward_headers = {
        k: v for k, v in request.headers.items()
        if k.lower() not in ("host", "content-length")
    }

    async with httpx.AsyncClient(timeout=10.0) as client:
        resp = await client.request(
            method=request.method,
            url=target,
            headers=forward_headers,
            content=body,
        )

    return Response(
        content=resp.content,
        status_code=resp.status_code,
        headers=dict(resp.headers),
    )
