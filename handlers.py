from aiogram import types, F, Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types.callback_query import CallbackQuery

import kb
import text
import utils
from states import Help


router = Router()


@router.message(Command("start"))
async def start_handler(msg: Message):
    if msg.chat.type == "private":
        await msg.answer(text.greet, reply_markup=kb.menu)


@router.message()
async def message_handler(msg: Message):
    # await msg.answer(f"Твой ID: {msg.from_user.id}")
    print(msg)


@router.callback_query(F.data == "help")
async def input_help(clbck: CallbackQuery, state: FSMContext):
    await state.set_state(Help.help)
    await clbck.message.edit_text(text.help)
