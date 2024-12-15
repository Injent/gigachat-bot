from typing import Final

from aiogram.fsm.context import FSMContext
from aiogram.types import Message

KEY_DISPOSE_STACK: Final[str] = 'dispose_stack'

async def append_dispose_stack(state: FSMContext, message_id: int):
    stack: list[int] = []

    if KEY_DISPOSE_STACK in (await state.get_data()).keys():
        stack = (await state.get_data()).get(KEY_DISPOSE_STACK)
    else:
        stack.append(message_id)
    await state.update_data(dispose_stack=stack)


async def dispose_messages(message: Message, state: FSMContext):
    await message.bot.delete_messages(
        chat_id=message.chat.id,
        message_ids=(await state.get_data()).get(KEY_DISPOSE_STACK)
    )
    await state.update_data(dispose_stack=[])