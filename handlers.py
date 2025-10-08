from aiogram import Bot
from aiogram import F
from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import CallbackQuery
from aiogram.types import Message
from aiogram.fsm.state import State
from aiogram.fsm.state import StatesGroup
import keyboard
from dotenv import load_dotenv
import os

load_dotenv()

router = Router()

class Ticket(StatesGroup):
    situation = State()
    cabinet = State()
    sender = State()
    confirm = State()
    answer = State()

@router.message(CommandStart())
async def start_command(message : Message):
    await message.answer('Здравствуйте! Нажмите на кнопку "✉️ Создать заявку", что бы обратится к ИТ-отделу',
                         reply_markup = keyboard.ticket_button)


@router.message(F.text == '✉️ Создать заявку')
async def situation_input(message : Message, state):
    await state.set_state(Ticket.situation)
    
    await message.answer('Опишите ситуацию')


@router.message(Ticket.situation)
async def cabinet_input(message : Message, state):
    await state.update_data(situation = message.text)
    await state.set_state(Ticket.cabinet)
    
    await message.answer('В каком кабинете это произошло?')


@router.message(Ticket.cabinet)
async def sender_input(message : Message, state):
    await state.update_data(cabinet = message.text)
    await state.set_state(Ticket.sender)

    await message.answer('Напишите @ВашЮзернейм / Номер телефона для связи')


@router.message(Ticket.sender)
async def confirm(message : Message, state):
    await state.update_data(sender = message.text)
    await state.set_state(Ticket.confirm)

    data = await state.get_data()

    await message.answer(f"Пожалуйста, проверьте данные перед отправкой :\n"
                         f"Описание ситуации : {data['situation']}\n"
                         f"Кабинет : {data['cabinet']}\n"
                         f"Отправитель : {data['sender']}", reply_markup = keyboard.confirm_buttons)
    

@router.callback_query(F.data == 'edit')
async def edit_ticket(callback : CallbackQuery, state):
    await state.clear()
    await state.set_state(Ticket.situation)

    await callback.message.edit_text('Опишите ситуацию')
    await callback.answer()


tickets = {}


@router.callback_query(F.data == 'confirm')
async def send_ticket(callback : CallbackQuery, state, bot : Bot):
    data = await state.get_data()

    sent = await bot.send_message(
        chat_id = os.getenv('CHAT_ID'),
        text=(
            f"📩 Новая заявка\n"
            f"Ситуация : {data['situation']}\n"
            f"Кабинет : {data['cabinet']}\n"
            f"Отправитель : {data['sender']}"
        ), reply_markup = keyboard.answer_button
    )

    tickets[sent.message_id] = callback.from_user.id

    await callback.message.edit_text("Заявка успешно отправлена, ожидайте ответа!")
    await state.clear()
    await callback.answer()


@router.callback_query(F.data == "answer")
async def answer(callback : CallbackQuery, state, bot : Bot):
    original_message = callback.message
    replied_id = original_message.message_id

    await state.update_data(ticket_id = replied_id)
    await state.set_state(Ticket.answer)

    await callback.message.answer("Напишите ответ на заявку : ")
    await callback.answer()


@router.message(Ticket.answer)
async def process_ticket_answer(message : Message, state, bot : Bot):
    data = await state.get_data()
    ticket_id = data["ticket_id"]

    if ticket_id in tickets:
        user_id = tickets[ticket_id]

        await bot.send_message(
            chat_id = user_id,
            text = (
                f"Ответ на вашу заявку:\n\n"
                f"{message.text}\n\n"
                f"От @{message.from_user.username}"
            )
        )

        await message.answer("Ваш ответ отправлен пользователю")

    await state.clear()