from sqlalchemy import insert

from database.database import session_factory
from database.models import User, ChatStyle, ChatAge, AnswerLength


async def create_user(user_id: int, name: str):
    async with session_factory() as s:
        if await s.get(User, user_id):
            return
        user = insert(User).values(
            id=user_id,
            display_name=name,
            chat_style=ChatStyle.none,
            chat_age=ChatAge.all,
            answer_length=AnswerLength.none,
            has_premium=False
        )
        await s.execute(user)
        await s.commit()


async def get_user(user_id: int) -> User:
    async with session_factory() as s:
        return await s.get(User, user_id)


async def set_premium(user_id: int, premium: bool):
    async with session_factory() as s:
        user = await s.get(User, user_id)

        user.has_premium = premium
        await s.commit()


async def has_premium(user_id: int) -> bool:
    async with session_factory() as s:
        user = await s.get(User, user_id)

        return user.has_premium


async def set_user_prefs(
        user_id,
        chat_style: [ChatStyle|None] = None,
        chat_age: [ChatAge|None] = None,
        answer_length: [AnswerLength|None] = None
):
    async with session_factory() as s:
        user = await s.get(User, user_id)

        if chat_style:
            user.chat_style = chat_style

        if chat_age:
            user.chat_age = chat_age

        if answer_length:
            user.answer_length = answer_length

        await s.commit()
