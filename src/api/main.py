from contextlib import asynccontextmanager
import asyncio
from fastapi import APIRouter, Depends, FastAPI
from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter
from starlette.middleware.cors import CORSMiddleware

from api.routers.auth import router as auth_router
from api.routers.orders import router as orders_router
from broker.consumer import rabbit_consumer
from broker.producer import rabbit_producer
from cache.client import redis_client


@asynccontextmanager
async def lifespan(_: FastAPI):
    await FastAPILimiter.init(redis_client.client)
    await rabbit_producer.connect()

    # там бесконечная таска
    asyncio.create_task(rabbit_consumer.connect())
    yield
    await FastAPILimiter.close()
    await rabbit_producer.close()
    await rabbit_consumer.close()


app = FastAPI(
    title="Order App API",
    lifespan=lifespan,
    dependencies=[Depends(RateLimiter(times=10, seconds=1))],
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

base_router = APIRouter(prefix="/api")
base_router.include_router(auth_router)
base_router.include_router(orders_router)

app.include_router(base_router)
