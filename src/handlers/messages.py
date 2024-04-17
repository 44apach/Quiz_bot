import asyncio
from aiogram.filters import Command, StateFilter
from aiogram.types import KeyboardButton, Message, ReplyKeyboardRemove
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram import Router, F, Bot
from dataclasses import dataclass

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from aiogram.types import FSInputFile

from decouple import config

# дописать удаление всео в конце

Admin = config("AdminId",default="")
BToken = config("Token", default="")

router = Router()

bot = Bot(token=BToken)

joinedFile = open("./src/joined_all.txt", "r")
joinedUsers = set ()
for line in joinedFile:
    joinedUsers.add(line.strip)
joinedFile.close()


class Quiz(StatesGroup):

    answering_first_question = State()
    answering_second_question = State()
    answering_third_question = State()


@router.message(Command("start"))
async def script_start(message: Message, state: FSMContext) -> None:

    if not str(message.chat.id) in joinedUsers:
            joinedFile = open("./src/joined_all.txt","a")
            joinedFile.write(str(message.chat.id)+"\n")
            joinedUsers.add(message.chat.id)       

    await message.answer("Вітаю, чим ви займайеся?")
    await state.set_state(Quiz.answering_first_question)    



@router.message(Quiz.answering_first_question)
async def second_question(message: Message, state: FSMContext) -> None:

    await state.update_data(answered_first = message.text.lower())
    await message.answer("Чи купували ви рекламу GoogleAds/FacebookAds?")
    await state.set_state(Quiz.answering_second_question)



@router.message(Quiz.answering_second_question)
async def third_question(message: Message, state: FSMContext) -> None:

    await state.update_data(answered_second = message.text.lower())
    await message.answer("Ви раніше пробували квіз?")
    await state.set_state(Quiz.answering_third_question)



@router.message(Quiz.answering_third_question)
async def quiz_finish(message: Message, state: FSMContext) -> None:

    user_data = await state.get_data()
    User = message.from_user.username
    UserId = message.from_user.id
    frst = user_data["answered_first"]
    sec = user_data["answered_second"]
    
    await bot.send_message(int(Admin),f"Відповіді\n\nId - {UserId}\nusername - @{User}\n\nперша відповідь - {frst}\n\nдруга відповідь - {sec}\n\nтретя відповідь - {message.text}\n")
    
    await state.clear()


