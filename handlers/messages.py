import aiofiles
from aiocsv import AsyncWriter
from loguru import logger
from aiogram import types
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, FSInputFile

from database.utils import write_new_product, get_user_products
from bot import telegram_router


@telegram_router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    await message.answer('Привет, это твой личный дневник питания! '
                         'Напишите слово "Добавить" и то что вы съели и я сохраню эту информацию для вас!')


@telegram_router.message(Command('help'))
async def cmd_help(message: Message) -> None:
    await message.answer('Напишите слово "Добавить" и то что вы съели и я сохраню эту информацию для вас!')


@telegram_router.message(Command('read'))
async def cmd_read(message: Message) -> None:
    products = await get_user_products(message.from_user.id)
    if not products:
        await message.answer('Вы ещё не добавляли продукты')
    else:
        result = []
        for product in products:
            result.append(': '.join(product))
        await message.answer('\n'.join(result))


@telegram_router.message(Command('get'))
async def cmd_get(message: Message) -> None:
    products = await get_user_products(message.from_user.id)
    if not products:
        await message.answer('Вы ещё не добавляли продукты')
    else:
        async with aiofiles.open(f'files/{message.from_user.id}.csv', 'w', newline='') as csv_file:
            writer = AsyncWriter(csv_file)
            await writer.writerows(products)
        await message.answer_document(FSInputFile(f'files/{message.from_user.id}.csv'))


@telegram_router.message()
async def add_product(message: types.Message) -> None:
    if message.text and message.text.lower().startswith(('добавить', 'добавь', 'add')):
        product = message.text.lower().split(' ')[1:]
        if not product:
            await message.answer('Вы не добавили ни одного продукта!')
        products = ' '.join(product)
        try:
            await write_new_product(message.date, message.from_user.id, products)
            await message.answer(f'Добавлено: {products}')
        except Exception as e:
            logger.error(f"Can't send message - {e}")
            await message.answer('Nice try!')
