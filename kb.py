from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


menu = [[InlineKeyboardButton(text="🔎 Помощь", callback_data="help")]]
menu = InlineKeyboardMarkup(inline_keyboard=menu)