import asyncio

from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

# import sys
# sys.path.append('../')

from config import BOT_TOKEN
from main import main
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


scrapper = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Забрать данные', callback_data='Парсить')]
])

router = Router()
bot = Bot(BOT_TOKEN)


@router.message(F.text == '/start')
async def step1(message: Message):
    await message.answer('Выберите подходящий пункт:', reply_markup=scrapper)


@router.callback_query(lambda callback_query: callback_query.data.startswith('Парсить'))
async def step1(message: Message):
    await message.answer(text='Произвожу парсинг ресурса, это займет пару минут')
    await main()
    await bot.send_message(chat_id=message.from_user.id, text='Выберите подходящий пункт:',
                           reply_markup=await kb.main_menu(callback.from_user.id))


@router.callback_query(lambda callback_query: callback_query.data.startswith('Админка'))
async def admin_menu(callback: CallbackQuery, bot):
    await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)
    await bot.send_message(chat_id=callback.from_user.id, text='Выберите подходящий пункт:',
                           reply_markup=kb.admin_menu)
