import redis
import json
from fastapi import APIRouter
import asyncio
from dotenv import dotenv_values
from concurrent.futures import ThreadPoolExecutor


env = dotenv_values(".env")

redis_host = env["REDIS_HOST"]
redis_port= env["REDIS_PORT"]

class RedisCache:
    def __init__(self):
        self.redis_url = (f"redis://{redis_host}:{redis_port}")
        self.redis = None
        self.executor = ThreadPoolExecutor(max_workers=4)

    def connect(self):
        self.redis = redis.from_url(self.redis_url)

    def disconnect(self):
        if self.redis is None:
            return
        self.redis.close()

    async def get(self, key: str):
        if self.redis is None:
            return
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(self.executor, self.redis.get, key)

    async def set(self, key: str, value: str, ex: int = 1):
        if self.redis is None:
            return
        loop = asyncio.get_event_loop()
        loop.run_in_executor(self.executor, self.redis.set, key, value, ex)


router = APIRouter()

redis_cache = RedisCache()

@router.on_event("startup")
async def startup_event():
    redis_cache.connect()

@router.on_event("shutdown")
async def shutdown_event():
    redis_cache.disconnect()

@router.get("/cache/{key}", tags=["Redis"])
async def get_from_cache(key: str):
    value = await redis_cache.get(key)
    if value is None:
        return {"message": "Key not found in cache"}
    return {"key": key, "value": value}

@router.post("/cache/{key}/{value}", tags=["Redis"])
async def set_to_cache(key: str, value: str, expiration: int = 1):
    value_json = json.dumps(value)
    await redis_cache.set(key, value_json, ex=expiration)
    return {"message": "Value set in cache", "key": key, "value": value}
