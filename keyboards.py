from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
import scrapper as scrap


available_resource_names = ["Металл", "Кожа", "Ткань", "Дерево", "Камень"]


def make_row_keyboard(items: list[str]) -> ReplyKeyboardMarkup:
    """
    Создаёт реплай-клавиатуру с кнопками в один ряд
    :param items: список текстов для кнопок
    :return: объект реплай-клавиатуры
    """
    row = [KeyboardButton(text=item) for item in items]
    return ReplyKeyboardMarkup(keyboard=[row], resize_keyboard=True)


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
