from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton

import logging


router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    logging.info(f"{message.chat.id}:{message.from_user.username}: {message.text}")

    keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="Поиск резюме")]], resize_keyboard=True
    )
    await message.answer(
        "Добро пожаловать! Нажмите кнопку ниже, чтобы начать поиск резюме",
        reply_markup=keyboard,
    )
