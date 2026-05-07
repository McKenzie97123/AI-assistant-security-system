import os
import json
import time
import logging
from dataclasses import dataclass

logger = logging.getLogger(__name__)

STRATEGY = os.getenv("PROTECTION_STRATEGY", "ml")
RATE_LIMIT_RPM = int(os.getenv("RATE_LIMIT_RPM", "60"))
DETECTION_THRESHOLD = float(os.getenv("DETECTION_THRESHOLD", "0.7"))

_BOT_UA_PATTERNS = ["python-requests", "curl", "wget", "scrapy", "aiohttp", "go-http", "java/"]


@dataclass
class AnalysisResult:
    blocked: bool
    score: float
    method: str
    reason: str


class RequestAnalyzer:
    def __init__(self, redis_client):
        self.redis = redis_client
        self.strategy = STRATEGY

        if self.strategy == "ml":
            from model import BotClassifier
            self.classifier = BotClassifier()
        elif self.strategy == "llm":
            import anthropic
            self.anthropic = anthropic.AsyncAnthropic()

    async def extract_features(self, request, body: bytes) -> dict:
        ip = request.client.host
        window_key = f"rate:{ip}:{int(time.time() / 60)}"
        count = await self.redis.incr(window_key)
        await self.redis.expire(window_key, 120)

        return {
            "ip": ip,
            "method": request.method,
            "path": str(request.url.path),
            "user_agent": request.headers.get("user-agent", ""),
            "content_type": request.headers.get("content-type", ""),
            "requests_per_minute": int(count),
            "has_accept_header": "accept" in request.headers,
            "has_accept_language": "accept-language" in request.headers,
            "body_size": len(body),
            "timestamp": time.time(),
        }

    async def analyze(self, features: dict) -> AnalysisResult:
        match self.strategy:
            case "rate_limit":
                return self._rate_limit(features)
            case "rules":
                return self._rules(features)
            case "ml":
                return self._ml(features)
            case "llm":
                return await self._llm(features)
            case _:
                return AnalysisResult(blocked=False, score=0.0, method="none", reason="")

    def _rate_limit(self, f: dict) -> AnalysisResult:
        rpm = f["requests_per_minute"]
        if rpm > RATE_LIMIT_RPM:
            return AnalysisResult(True, 1.0, "rate_limit", f"rpm={rpm}")
        return AnalysisResult(False, rpm / RATE_LIMIT_RPM, "rate_limit", "")

    def _rules(self, f: dict) -> AnalysisResult:
        score, reasons = 0.0, []

        if f["requests_per_minute"] > 30:
            score += 0.4
            reasons.append("high_rate")

        ua = f["user_agent"].lower()
        if any(p in ua for p in _BOT_UA_PATTERNS):
            score += 0.4
            reasons.append("bot_ua")

        if not f["has_accept_header"]:
            score += 0.1
            reasons.append("no_accept")

        if not f["has_accept_language"]:
            score += 0.1
            reasons.append("no_accept_lang")

        blocked = score >= DETECTION_THRESHOLD
        return AnalysisResult(blocked, score, "rules", ",".join(reasons) if blocked else "")

    def _ml(self, f: dict) -> AnalysisResult:
        score = self.classifier.predict_proba(f)
        blocked = score >= DETECTION_THRESHOLD
        return AnalysisResult(blocked, score, "ml", "ml_detection" if blocked else "")

    async def _llm(self, f: dict) -> AnalysisResult:
        features_str = json.dumps(
            {k: v for k, v in f.items() if k not in ("ip", "timestamp")},
            indent=2,
        )
        response = await self.anthropic.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=64,
            system=(
                "You are a bot detection system. Analyze HTTP request features and respond with "
                "exactly one of: BOT:<score> or HUMAN:<score> where score is 0.00-1.00. Nothing else."
            ),
            messages=[{"role": "user", "content": f"Features:\n{features_str}"}],
        )
        text = response.content[0].text.strip()
        try:
            verdict, score_str = text.split(":")
            score = float(score_str)
            blocked = verdict == "BOT" and score >= DETECTION_THRESHOLD
        except Exception:
            blocked, score = False, 0.0

        return AnalysisResult(blocked, score, "llm", "llm_detection" if blocked else "")
