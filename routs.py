from typing import Annotated

from aiogram import types
from fastapi import APIRouter, Header
from loguru import logger

from bot import bot, dp
from config import settings

root_router = APIRouter(
    prefix='',
    tags=['root'],
    responses={404: {'description': 'Not found'}},
)


@root_router.get("/")
async def root() -> dict:
    return {"message": "Hello World"}


@root_router.post('/')
async def bot_webhook(update: dict,
                      x_telegram_bot_api_secret_token: Annotated[str | None, Header()] = None) -> None | dict:
    logger.info(update)
    if x_telegram_bot_api_secret_token != settings.my_token:
        logger.error("Wrong secret token !")
        return {"status": "error", "message": "Wrong secret token !"}
    telegram_update = types.Update(**update)
    await dp.feed_webhook_update(bot=bot, update=telegram_update)
