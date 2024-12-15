from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, Message, ReplyKeyboardRemove

from database.methods.user import set_user_prefs, get_user
from handlers.menu import set_menu_message
from keyboards.keyboards_utils import create_one_select_keyboard, create_double_column_keyboard
from states.state import SettingsState
from util.context_prompts import CHAT_STYLES, CHAT_AGE, ANSWER_LENGTH, get_option_by_name

router = Router()


@router.callback_query(F.data == 'settings')
async def settings(callback: CallbackQuery, state: FSMContext):
    await __set_settings__(callback.message, state)


@router.callback_query(SettingsState.main, F.data == 'chat_style')
async def chat_style(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(
        text='Укажите стиль ответа:',
        reply_markup=create_double_column_keyboard(actions=CHAT_STYLES.values())
    )
    await state.set_state(SettingsState.input_chat_style)


@router.callback_query(SettingsState.main, F.data == 'chat_age')
async def chat_age(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(
        text='Укажите возраст ответа:',
        reply_markup=create_one_select_keyboard(options=CHAT_AGE.values())
    )
    await state.set_state(SettingsState.input_chat_age)


@router.callback_query(SettingsState.main, F.data == 'answer_length')
async def answer_length(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(
        text='Укажите длину ответа:',
        reply_markup=create_one_select_keyboard(options=ANSWER_LENGTH.values())
    )
    await state.set_state(SettingsState.input_answer_length)


@router.message(SettingsState.input_chat_style)
async def accept_chat_style(message: Message, state: FSMContext):
    style = message.text

    if style not in CHAT_STYLES.values():
        await message.answer(text='Такого вырианта не существует',)
        return

    await set_user_prefs(user_id=message.chat.id, chat_style=get_option_by_name(CHAT_STYLES, style))
    await __apply_settings__(message, state)


@router.message(SettingsState.input_chat_age)
async def accept_chat_age(message: Message, state: FSMContext):
    age = message.text

    if age not in CHAT_AGE.values():
        await message.answer(text='Такого вырианта не существует')
        return

    await set_user_prefs(user_id=message.chat.id, chat_age=get_option_by_name(CHAT_AGE, age))
    await __apply_settings__(message, state)


@router.message(SettingsState.input_answer_length)
async def accept_answer_length(message: Message, state: FSMContext):
    length = message.text

    if length not in ANSWER_LENGTH.values():
        await message.answer(text='Такого вырианта не существует')
        return

    await set_user_prefs(user_id=message.chat.id, answer_length=get_option_by_name(ANSWER_LENGTH, length))
    await __apply_settings__(message, state)


async def __apply_settings__(message: Message, state: FSMContext):
    await message.answer(
        text='✅ Настройки сохранены',
        reply_markup=ReplyKeyboardRemove()
    )
    await __set_settings__(message, state)


async def __set_settings__(message: Message, state: FSMContext):
    user = await get_user(message.chat.id)

    await message.bot.send_message(
        text=f'⚙️   ------====== НАСТРОЙКИ ======------   ⚙️\n\n'
             f'Стиль: {CHAT_STYLES[user.chat_style]}\n'
             f'Возрастная категория: {CHAT_AGE[user.chat_age]}\n'
             f'Длина ответа: {ANSWER_LENGTH[user.answer_length]}\n',
        chat_id=message.chat.id,
        reply_markup=__create_settings_keyboard__(),
    )

    await state.set_state(SettingsState.main)


def __create_settings_keyboard__() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='Стиль ответа', callback_data='chat_style')],
            [InlineKeyboardButton(text='Возрастная категория', callback_data='chat_age')],
            [InlineKeyboardButton(text='Длина ответа', callback_data='answer_length')],
            [InlineKeyboardButton(text='Назад', callback_data='menu')]
        ]
    )
