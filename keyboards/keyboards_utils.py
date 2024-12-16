from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder


# Создание клавиатуры с двумя колонками
def create_double_column_keyboard(actions: list[str]) -> ReplyKeyboardMarkup:
    keyboard = []
    row = []
    for i, button_text in enumerate(actions):
        row.append(KeyboardButton(text=button_text))
        if len(row) == 2:
            keyboard.append(row)
            row = []

    keyboard.append(row)
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


# Создание клавиатуры в колонку
def create_one_select_keyboard(options: list[str]) -> ReplyKeyboardMarkup:
    keyboard: list[list[KeyboardButton]] = []

    for option in options:
        keyboard.append([KeyboardButton(text=option)])

    return ReplyKeyboardMarkup(
        keyboard=keyboard
    )