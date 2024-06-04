from aiogram import F, Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types.callback_query import CallbackQuery
from datetime import datetime as dt

import kb
import text
import utils
from db import (
    get_placement_by_address, 
    get_detector_by_name_placement,
    get_companies_chats_by_placementd_id
)
from states import Help
from main import bot


router = Router()


@router.message(Command("start"))
async def start_handler(msg: Message):
    if msg.chat.type == "private":
        await msg.answer(text.greet, reply_markup=kb.menu)


@router.message()
async def message_handler(msg: Message):
    pass


@router.callback_query(F.data == "help")
async def input_help(clbck: CallbackQuery, state: FSMContext):
    await state.set_state(Help.help)
    await clbck.message.edit_text(text.help)


async def send_mqtt_alert(data: dict):
    placement = await get_placement_by_address(data["address"])

    if placement:
        placement_id = placement[0][0]
        detector = await get_detector_by_name_placement(data["device"], placement_id)
       
        if detector:
            companies_chats = await get_companies_chats_by_placementd_id(placement_id)
            
            for company_chat in companies_chats:
                time = dt.now().strftime("%Y-%m-%d %H:%M:%S")
                msg = text.alert.format(
                    placement[0][1],
                    detector[0][1],
                    data["avg-gas-value"],
                    data["threshold"],
                    time,
                    company_chat[0]
                )
                await bot.send_message(company_chat[1], msg)
