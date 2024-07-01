from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
import scrapper as scrap


available_resource_names = ["Металл", "Кожа", "Ткань", "Дерево", "Камень"]


start_parsing = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Начать парсинг', callback_data='start_parsing')]
])


change_resource = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Металл', callback_data='metal')],
    [InlineKeyboardButton(text='Кожа', callback_data='leather')],
    [InlineKeyboardButton(text='Ткань', callback_data='cloth')],
    [InlineKeyboardButton(text='Дерево', callback_data='wood')],
    [InlineKeyboardButton(text='Камень', callback_data='stone')],
])


change_other_town = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Да', callback_data='other_towns'),
     InlineKeyboardButton(text='Нет', callback_data='one_town')],
])


async def other_town() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text='Личный кабинет', callback_data='Личный_кабинет')],
        [InlineKeyboardButton(text='Информация', callback_data='Информация')]
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)
