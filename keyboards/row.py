from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def make_row_keyboard(items: list[str]) -> ReplyKeyboardMarkup:
    """
    Создаёт реплай-клавиатуру с кнопками в несколько рядов
    :param items: список текстов для кнопок
    :return: объект реплай-клавиатуры
    """
    builder = ReplyKeyboardBuilder()
    for item in items:
        builder.row(KeyboardButton(text=item))
    return builder.as_markup()
