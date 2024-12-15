from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

router = Router()

@router.callback_query(F.data == 'help')
async def process_help(callback: CallbackQuery):
    await callback.message.answer(
        text='🤖   ------====== Тех. поддержка ======------   🤖\n\nНапишите @Injent если возникли трудности с '
             'использованием или ошибки',
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text='Назад', callback_data='menu')]
            ]
        )
    )