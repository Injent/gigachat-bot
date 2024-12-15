from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton

from database.methods.user import get_user
from external_services.gigachat import answer_gigachat
from keyboards.keyboards_utils import create_double_column_keyboard
from states.state import PromptState
from util.context_prompts import create_prompt, CHAT_STYLES, CHAT_AGE, ANSWER_LENGTH

characters = [
    'Инженер с 30 летним опытом',
    'UI дизайнер с 30 летним опытом',
    'Художник с 30 летним опытом',
    'Экономист с 30 летним опытом',
    'Юрист с 30 летним опытом'
]

formats = [
    'Группированный',
    'Разбитый на блоки',
    'Плюсы и минусы',
    'Без формата'
]

text_actions = [
    'Анализировать',
    'Обобщить',
    'Классифицировать',
    'Логически рассудить'
]


router = Router()


@router.callback_query(F.data == 'ask')
async def ask(callback: CallbackQuery, state: FSMContext):
    await state.set_state(PromptState.param_action)
    await callback.message.answer(
        text='Что нужно сделать с текстом?',
        reply_markup=create_double_column_keyboard(actions=text_actions)
    )


@router.message(PromptState.param_action)
async def ask(message: Message, state: FSMContext):
    await state.set_state(PromptState.param_character)
    await state.update_data(action=message.text)
    await message.answer(
        text='Напишите от чьего лица будет ответ?',
        reply_markup=create_double_column_keyboard(actions=characters)
    )

@router.message(PromptState.param_character)
async def process_character(message: Message, state: FSMContext):
    await state.set_state(PromptState.param_format)
    await state.update_data(character=message.text)
    await message.answer(
        text='В каком формате хотите получить ответ?',
        reply_markup=create_double_column_keyboard(actions=formats)
    )


@router.message(PromptState.param_format)
async def process_format(message: Message, state: FSMContext):
    await state.update_data(format=message.text)
    await state.set_state(PromptState.question)
    await message.answer(
        text='Напишите ваш запрос',
        reply_markup=ReplyKeyboardRemove()
    )


@router.message(PromptState.question)
async def process_question(message: Message, state: FSMContext):
    user = await get_user(message.chat.id)
    data = await state.get_data()
    action = data['action']
    character = data['character']
    form = data['format']
    question = message.text

    prompt = create_prompt(
        text=question,
        action=action,
        style=CHAT_STYLES[user.chat_style],
        age=CHAT_AGE[user.chat_age],
        length=ANSWER_LENGTH[user.answer_length],
        char=character,
        form=form
    )
    m_id = (await message.bot.send_message(
        chat_id=message.chat.id,
        text='Обработка текста...'
    )).message_id

    response = await answer_gigachat(prompt)
    await message.bot.edit_message_text(
        text=response,
        chat_id=message.chat.id,
        message_id=m_id
    )
    await message.bot.edit_message_reply_markup(
        chat_id=message.chat.id,
        message_id=m_id,
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text='Назад', callback_data='menu')]
            ]
        )
    )
