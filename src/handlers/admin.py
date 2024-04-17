from aiogram import Router, F, Bot
import asyncio
from aiogram.filters import Command
from aiogram.types import Message
from decouple import config 

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from aiogram.exceptions import TelegramForbiddenError


Admin = config("AdminId", default="")
BToken = config("Token", default="")

router = Router()

bot = Bot(token=BToken)

class AdminCommands(StatesGroup):
    
    Admin_enter_state = State()
    Admin_msg_state = State()


@router.message(Command("admin"))
async def Admin_enter(message: Message, state: FSMContext) -> None:

    CurrentUser = message.from_user.id

    if CurrentUser == int(Admin):
            await state.set_state(AdminCommands.Admin_enter_state)
            await message.answer(f"Команди:\n\n /update - актуалізація користувачів боту")
                
    else:
        return None
        


@router.message(AdminCommands.Admin_enter_state, Command("update"))
async def Update_Users(message: Message, state: FSMContext):

# прописать кнопки для подтверждения
    with open("./src/joined_all.txt", "r") as in_file:
        lines = in_file.readlines()
        set_unique = set()

        set_unique.update(lines)
        
    with open("./src/joined_all.txt", "w") as out_file:
        for line in set_unique:
            try:
                await bot.send_chat_action(int(line),action="typing")
                out_file.write(str(line))
            except TelegramForbiddenError:
                    out_file.write("-\n")
                    continue
            except ValueError:
                    continue
            
    await message.answer("Користувачі актуалізовані, переходьте до /sendAll")        
        

@router.message(AdminCommands.Admin_enter_state, Command("sendAll"))
async def NewText(message: Message, state: FSMContext):
    await message.answer("Напишіть текст до розсилки")
    await state.set_state(AdminCommands.Admin_msg_state)


@router.message(AdminCommands.Admin_msg_state,F.text)
async def Send_All(message: Message, state: FSMContext):

    text = message.text
    await message.answer(f"Ось текст розсилки \n\n{text}")

    with open("./src/joined_all.txt", "r") as file:
        lines = file.readlines()

        for line in lines:
            try:
                await bot.send_message(int(line), text)
            except ValueError:
                continue 
            except int(line) == int(Admin):
                continue

    await message.answer("все відправлено")    