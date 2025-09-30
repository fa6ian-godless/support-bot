from aiogram.types import ReplyKeyboardMarkup
from aiogram.types import KeyboardButton
from aiogram.types import InlineKeyboardMarkup
from aiogram.types import InlineKeyboardButton

ticket_button = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='✉️ Создать заявку')]], resize_keyboard=True)

confirm_buttons = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Изменить', callback_data="edit")],
    [InlineKeyboardButton(text='Подтвердить', callback_data="confirm")]])

answer_button = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Ответить", callback_data="answer")]
])