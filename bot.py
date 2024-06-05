from aiogram import Bot, Router, Dispatcher
from aiogram.types import WebhookInfo, BotCommand
from loguru import logger

from config import settings


telegram_router = Router(name='telegram')
dp = Dispatcher()
dp.include_router(telegram_router)


bot = Bot(token=settings.api_token)


async def set_webhook(my_bot: Bot) -> None:
    async def check_webhook() -> WebhookInfo | None:
        try:
            webhook_info = await my_bot.get_webhook_info()
            return webhook_info
        except Exception as e:
            logger.error(f"Can not get webhook info! {e}")
            return

    current_webhook_info = await check_webhook()
    logger.debug(f'Current webhook info: {current_webhook_info}')
    try:
        await bot.set_webhook(
            f'{settings.webhook_url}{settings.webhook_path}',
            secret_token=settings.my_token,
            drop_pending_updates=current_webhook_info.pending_update_count > 0,
            max_connections=40,
        )
        logger.debug(f"Updated bot info: {await check_webhook()}")
    except Exception as e:
        logger.error(f"Can not set webhook! {e}")


async def set_bot_commands_menu(my_bot: Bot) -> None:
    commands = [
        BotCommand(command='/start', description='Начать'),
        BotCommand(command='/help', description='Помощь'),
        BotCommand(command='/read', description='Прочитать дневник'),
        BotCommand(command='/get', description='Получить дневник файлом'),
    ]
    try:
        await my_bot.set_my_commands(commands)
    except Exception as e:
        logger.error(f"Can't set commands! {e}")


async def start_telegram():
    logger.debug('Set webhook')
    await set_webhook(bot)
    logger.debug('Set commands')
    await set_bot_commands_menu(bot)


async def on_shutdown():
    await bot.delete_webhook()
    logger.debug('webhook deleted')

