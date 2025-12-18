import aiohttp
import asyncio
import logging
from typing import List, Optional, Any, Dict
from .models import RetrievalResult, RetrievalQuery
from .config import RetrievalConfig
from .exceptions import RetrievalError, APIError, TimeoutError, ValidationError, ConfigError

logger = logging.getLogger(__name__)

class RetrievalClient:
    def __init__(self, config: RetrievalConfig):
        self.config = config
        self.session: Optional[aiohttp.ClientSession] = None

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def health_check(self) -> bool:
        if not self.session:
            raise RuntimeError("Use 'async with' to initialize client")
        try:
            async with self.session.get(self.config.vlm_rag_endpoint.replace("/api/search", "/api/health"), timeout=self.config.timeout_seconds) as resp:
                return resp.status == 200
        except Exception as e:
            logger.warning(f"Health check failed: {e}")
            return False

    async def search(self, query: str, video_id: Optional[str] = None, top_k: Optional[int] = None, threshold: Optional[float] = None, filters: Optional[Dict[str, Any]] = None) -> List[RetrievalResult]:
        if not self.session:
            raise RuntimeError("Use 'async with' to initialize client")
        rq = RetrievalQuery(query=query, top_k=top_k or self.config.default_top_k, threshold=threshold or self.config.default_threshold, filters=filters)
        payload = {
            "query": rq.query,
            "video_id": video_id,
            "top_k": rq.top_k,
            "threshold": rq.threshold
        }
        if rq.filters:
            payload["filters"] = rq.filters
        headers = {"Authorization": f"Bearer {self.config.vlm_rag_api_key}"} if self.config.vlm_rag_api_key else {}
        async def _call_api():
            async with self.session.post(self.config.vlm_rag_endpoint, json=payload, headers=headers, timeout=self.config.timeout_seconds) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    return data
                else:
                    text = await resp.text()
                    raise APIError(f"API error {resp.status}: {text}")
        try:
            raw = await self._retry_with_backoff(_call_api)
            return self.parse_results(raw)
        except asyncio.TimeoutError:
            logger.warning(f"Timeout for query: {query}")
            return []
        except APIError as e:
            logger.error(f"API error: {e}")
            return []
        except Exception as e:
            logger.error(f"Unexpected error: {e}", exc_info=True)
            return []

    async def _retry_with_backoff(self, func, max_retries: Optional[int] = None, base_delay: Optional[float] = None):
        max_retries = max_retries if max_retries is not None else self.config.max_retries
        base_delay = base_delay if base_delay is not None else self.config.retry_base_delay
        for attempt in range(max_retries):
            try:
                return await func()
            except (aiohttp.ClientError, asyncio.TimeoutError) as e:
                if attempt == max_retries - 1:
                    raise
                delay = min(base_delay * (2 ** attempt), self.config.retry_max_delay)
                logger.warning(f"Retry {attempt+1}/{max_retries} after {delay}s: {e}")
                await asyncio.sleep(delay)

    def parse_results(self, raw_response: dict) -> List[RetrievalResult]:
        results = []
        items = raw_response.get("results", [])
        for item in items:
            try:
                result = RetrievalResult(
                    id=item.get("segment_id") or item.get("id"),
                    score=float(item.get("score", 0)),
                    content=item.get("summary") or item.get("content") or "",
                    metadata=item.get("metadata"),
                    timestamp=None
                )
                results.append(result)
            except Exception as e:
                logger.warning(f"Failed to parse result item: {item} | {e}")
        logger.info(f"Retrieved {len(results)} results")
        return results
