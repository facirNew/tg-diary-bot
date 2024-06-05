from fastapi import FastAPI
from contextlib import asynccontextmanager
from loguru import logger

from bot import start_telegram, on_shutdown
from routs import root_router
import handlers # NOQA


@asynccontextmanager
async def lifespan(application: FastAPI):
    logger.info('Start application')
    await start_telegram()
    yield
    await on_shutdown()
    logger.info('Stop application')


app = FastAPI(lifespan=lifespan)
app.include_router(root_router)
