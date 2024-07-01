import asyncio
from bs4 import BeautifulSoup

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
from scrapper import get_html, xpath_resources, town_click, material_pars
from add_to_table import add_value


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
    other_towns = State()
    a_town = State()
    sale = State()
    recycling = State()
    materials = State()
    resources = State()
    tax = State()


@router.message(F.text == '/start')
async def cmd_food(message: Message):
    await message.answer('Начнитие парсинг:', reply_markup=kb.start_parsing)


@router.callback_query(lambda callback_query: callback_query.data.startswith('start_parsing'))
async def step1(message: Message):
    await bot.send_message(chat_id=message.from_user.id, text=f'Выберите критерии парсинга',
                           reply_markup=kb.change_resource)


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
    await state.update_data(other_town=False)
    await state.set_state(Filters.tax)
    await state.set_state(Filters.a_town)
    await bot.send_message(chat_id=message.from_user.id, text=f"Выберите город из списка и введите его номер: "
                                f"\n1: Bridgewatch \n2: Caerleon \n3: Fort Sterling "
                                f"\n4: Lymhurst \n5: Martlock \n6: Thetford \n7: Brecilien")


@router.message(Filters.a_town)
async def save_name(callback: CallbackQuery, state: FSMContext):
    await state.update_data(a_town=towns[callback.text])
    await state.set_state(Filters.tax)
    await callback.bot.send_message(chat_id=callback.chat.id, text=f"Вы выбрали {towns[callback.text]}\n"
                                                                   f"Теперь укажите налог:")


@router.callback_query(lambda callback_query: callback_query.data.startswith('other_towns'))
async def step1(message: Message, state: FSMContext):
    await state.update_data(other_town=True)
    await state.set_state(Filters.sale)
    await bot.send_message(chat_id=message.from_user.id,
                           text=f"Продажа материалов. \nВведите номер города: "
                                f"\n1: Bridgewatch \n2: Caerleon \n3: Fort Sterling "
                                f"\n4: Lymhurst \n5: Martlock \n6: Thetford \n7: Brecilien")


@router.message(Filters.sale)
async def save_name(callback: CallbackQuery, state: FSMContext):
    await state.update_data(sale=towns[callback.text])
    await state.set_state(Filters.recycling)
    await callback.bot.send_message(chat_id=callback.chat.id, text=f"Переработка. \nВведите номер города: "
                                f"\n1: Bridgewatch \n2: Caerleon \n3: Fort Sterling "
                                f"\n4: Lymhurst \n5: Martlock \n6: Thetford \n7: Brecilien")


@router.message(Filters.recycling)
async def save_name(callback: CallbackQuery, state: FSMContext):
    await state.update_data(recycling=towns[callback.text])
    await state.set_state(Filters.materials)
    await callback.bot.send_message(chat_id=callback.chat.id, text=f"Покупка материалов. \nВведите номер города: "
                                f"\n1: Bridgewatch \n2: Caerleon \n3: Fort Sterling "
                                f"\n4: Lymhurst \n5: Martlock \n6: Thetford \n7: Brecilien")


@router.message(Filters.materials)
async def save_name(callback: CallbackQuery, state: FSMContext):
    await state.update_data(materials=towns[callback.text])
    await state.set_state(Filters.resources)
    await callback.bot.send_message(chat_id=callback.chat.id, text=f"Покупка ресурсов. \nВведите номер города: "
                                f"\n1: Bridgewatch \n2: Caerleon \n3: Fort Sterling "
                                f"\n4: Lymhurst \n5: Martlock \n6: Thetford \n7: Brecilien")


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
    other_town = data['other_town']

    xpath_resource = xpath_resources.get(resource)
    if other_town:
        sale = data['sale']
        recycling = data['recycling']
        materials = data['materials']
        resources = data['resources']
        tax = data['tax']
        other_towns_xpath = [town_click[sale], town_click[recycling],
                             town_click[materials], town_click[resources]]

        await callback.bot.send_message(chat_id=callback.chat.id,
                                        text=f'Вы выбрали следующие параметры для парсинга: '
                                             f'\nРесурс для парсинга: {resource}, '
                                             f'\nПродажа материалов:{sale}, \nПереработка: {recycling}, '
                                             f'\nПокупка материалов: {materials}, \nПокупка ресурсов: {resources}, '
                                             f'\nНалог: {tax}',
                                        reply_markup=kb.start_parsing)

        html = await get_html(xpath_resource, tax, other_towns_xpath=other_towns_xpath)
        table_data = await material_pars(html)
        await add_value(table_data, 2)

        await callback.bot.send_message(chat_id=callback.chat.id,
                                        text=f'Данные загружены в таблицу, можете попробовать снова',
                                        reply_markup=kb.start_parsing)
    else:
        a_town = data['a_town']
        tax = data['tax']
        await callback.bot.send_message(chat_id=callback.chat.id,
                                        text=f'Вы выбрали следующие параметры для парсинга: \n'
                                             f'Ресурс для парсинга: {resource}, \nНалог: {tax}')

        html = await get_html(xpath_resource, tax, a_town=town_click[a_town])
        table_data = await material_pars(html)
        await add_value(table_data, 2)

        await callback.bot.send_message(chat_id=callback.chat.id,
                                        text=f'Данные загружены в таблицу, можете попробовать снова',
                                        reply_markup=kb.start_parsing)
