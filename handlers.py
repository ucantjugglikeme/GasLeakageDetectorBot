from aiogram import types, F, Router
from aiogram.types import Message
from aiogram.filters import Command


router = Router()


@router.message(Command("start"))
async def start_handler(msg: Message):
    await msg.answer(
        "Привет! Я оповещаю пользователей о происшествиях помощью устройства обнаружения утечек газа!\n"
        "Чтобы начать пользоваться мной, добавьте меня в беседу и свяжитесь со своим менеджером."
    )


@router.message()
async def message_handler(msg: Message):
    # await msg.answer(f"Твой ID: {msg.from_user.id}")
    print(msg)
