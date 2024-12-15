from uuid import uuid4

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, LabeledPrice, PreCheckoutQuery, \
    Message

from config_data.config import config
from database.methods.user import set_premium
from handlers.menu import set_menu_message

router = Router()



@router.callback_query(F.data == 'payments')
async def payment(callback: CallbackQuery):
    await callback.message.answer_invoice(
        title='Оплата GigaChat Pro',
        description='Быстрее обрабатывает запросы и дает ответы более точно',
        payload=str(uuid4()),
        provider_token=config.tg_bot.payment_token,
        currency='RUB',
        prices=[
            LabeledPrice(label='GigaChat Pro', amount=400_00)
        ],
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text='Купить', pay=True)],
                [InlineKeyboardButton(text='Назад', callback_data='menu')]
            ]
        )
    )


@router.pre_checkout_query()
async def process_pre_checkout_query(query: PreCheckoutQuery):
    await query.bot.answer_pre_checkout_query(pre_checkout_query_id=query.id, ok=True)


@router.message(F.successful_payment)
async def success_plan_upgrade(message: Message, state: FSMContext):
    await set_premium(user_id=message.chat.id, premium=True)
    await set_menu_message(message, state)