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
import keyboards as kb


router = Router()
bot = Bot(BOT_TOKEN)


towns = {
            '1': "Bridgewatch",
            '2': "Caerleon",
            '3': "Fort Sterling",
            '4': "Lymhurst",
            '5': "Martlock",
            '6': "Thetford",
            '7': "Brecilien"
}


class Filters(StatesGroup):
    resource = State()
    sale = State()
    recycling = State()
    materials = State()
    resources = State()
    tax = State()


@router.message(F.text == '/start')
async def cmd_food(message: Message):
    await message.answer('Выберите ресурс:', reply_markup=kb.change_resource)


@router.callback_query(lambda callback_query: callback_query.data.startswith('metal'))
async def step1(message: Message, state: FSMContext):
    await state.update_data(resource='metal')
    await bot.send_message(chat_id=message.from_user.id, text=f'Использовать ли цены из разных городов?',
                           reply_markup=kb.change_other_town)


@router.callback_query(lambda callback_query: callback_query.data.startswith('leather'))
async def step1(message: Message, state: FSMContext):
    await state.update_data(resource='leather')
    await bot.send_message(chat_id=message.from_user.id, text=f'Использовать ли цены из разных городов?',
                           reply_markup=kb.change_other_town)


@router.callback_query(lambda callback_query: callback_query.data.startswith('cloth'))
async def step1(message: Message, state: FSMContext):
    await state.update_data(resource='cloth')
    await bot.send_message(chat_id=message.from_user.id, text=f'Использовать ли цены из разных городов?',
                           reply_markup=kb.change_other_town)


@router.callback_query(lambda callback_query: callback_query.data.startswith('wood'))
async def step1(message: Message, state: FSMContext):
    await state.update_data(resource='wood')
    await bot.send_message(chat_id=message.from_user.id, text=f'Использовать ли цены из разных городов?',
                           reply_markup=kb.change_other_town)


@router.callback_query(lambda callback_query: callback_query.data.startswith('stone'))
async def step1(message: Message, state: FSMContext):
    await state.update_data(resource='stone')
    await bot.send_message(chat_id=message.from_user.id, text=f'Использовать ли цены из разных городов?',
                           reply_markup=kb.change_other_town)


@router.callback_query(lambda callback_query: callback_query.data.startswith('one_town'))
async def step1(message: Message, state: FSMContext):
    await state.update_data(other_town=None)
    await state.set_state(Filters.tax)
    await bot.send_message(chat_id=message.from_user.id, text=f'Укажите размер налога')


@router.callback_query(lambda callback_query: callback_query.data.startswith('other_towns'))
async def step1(message: Message, state: FSMContext):
    await state.set_state(Filters.sale)
    await bot.send_message(chat_id=message.from_user.id, text=f'Продажа материалов. \nВведите номер города: {towns}')


@router.message(Filters.sale)
async def save_name(callback: CallbackQuery, state: FSMContext):
    await state.update_data(sale=towns[callback.text])
    await state.set_state(Filters.recycling)
    await callback.bot.send_message(chat_id=callback.chat.id, text=f'Переработка. \nВведите номер города: {towns}')


@router.message(Filters.recycling)
async def save_name(callback: CallbackQuery, state: FSMContext):
    await state.update_data(recycling=towns[callback.text])
    await state.set_state(Filters.materials)
    await callback.bot.send_message(chat_id=callback.chat.id, text=f'Покупка материалов. \nВведите номер города: {towns}')


@router.message(Filters.materials)
async def save_name(callback: CallbackQuery, state: FSMContext):
    await state.update_data(materials=towns[callback.text])
    await state.set_state(Filters.resources)
    await callback.bot.send_message(chat_id=callback.chat.id, text=f'Покупка ресурсов. \nВведите номер города: {towns}')


@router.message(Filters.resources)
async def save_name(callback: CallbackQuery, state: FSMContext):
    await state.update_data(resources=towns[callback.text])
    await state.set_state(Filters.tax)
    await callback.bot.send_message(chat_id=callback.chat.id, text=f'Укажите размер налога:')


@router.message(Filters.tax)
async def save_name(callback: CallbackQuery, state: FSMContext):
    await state.update_data(tax=callback.text)
    data = await state.get_data()
    resource = data['resource']
    sale = data['sale']
    recycling = data['recycling']
    materials = data['materials']
    resources = data['resources']
    tax = data['tax']
    await callback.bot.send_message(chat_id=callback.chat.id, text=f'Вы выбрали следующие параметры для парсинга: \n'
                                                                   f'{resource}, {sale}, {recycling}, {materials}, '
                                                                   f'{resources}, {tax}')

