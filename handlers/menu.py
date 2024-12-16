from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

from database.methods.user import create_user, has_premium
from states.state import MenuState

router = Router()


# Отображение меню на /start
@router.message(CommandStart())
async def welcome(message: Message, state: FSMContext):
    await message.delete()
    await create_user(user_id=message.from_user.id, name=message.from_user.full_name)
    await set_menu_message(message, state)


# Отображение меню по колбэк
@router.callback_query(F.data == 'menu')
async def menu(callback: CallbackQuery, state: FSMContext):
    await set_menu_message(callback.message, state)


# Отправка сообщения с меню
async def set_menu_message(
        message: Message,
        state: FSMContext
) -> int:
    await state.set_state(MenuState.main)
    premium = await has_premium(message.chat.id)

    m = await message.bot.send_message(
        text=__create_main_menu_text__(premium),
        chat_id=message.chat.id,
        reply_markup=__create_main_menu_keyboard__(premium)
    )
    return m.message_id


# Функции утилиты для создания контента для сообщения menu
def __create_main_menu_text__(premium: bool) -> str:
    if premium:
        status = '🥇 Pro версия GigaChat'
    else:
        status = '🧩 Обычная версия GigaChat'

    return (f'✨ ------====== МЕНЮ ======------ ✨\n\n{status}\n\nЗадайте вопрос GigaChat используя конструктор'
            f' запросов (можно настроить в ⚙️)')


def __create_main_menu_keyboard__(premium: bool) -> InlineKeyboardMarkup:
    middle_row = [InlineKeyboardButton(text='🛠️ Тех. поддержка', callback_data='help')]

    if not premium:
        middle_row.append(InlineKeyboardButton(text='💸 Купить GigaChat Pro', callback_data='payments'))

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='⚙️ Настройки', callback_data='settings')],
            middle_row,
            [InlineKeyboardButton(text='✨ Сообщение для GigaChat', callback_data='ask')],
        ]
    )