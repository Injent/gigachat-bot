import enum
from typing import Annotated

from sqlalchemy import Column, Enum
from sqlalchemy.orm import mapped_column, Mapped

from database.database import Base

pk = Annotated[int, mapped_column(primary_key=True)]


class ChatAge(enum.Enum):
    all = 0
    child = 1
    teenage = 2
    adult = 3


class ChatStyle(enum.Enum):
    none = 0
    story = 1
    description = 2
    convincing = 3
    creative = 4
    official = 5


class AnswerLength(enum.Enum):
    none = 0
    short = 1
    normal = 2
    full = 3


class User(Base):
    __tablename__ = 'user'

    id: Mapped[pk]
    display_name: Mapped[str]
    chat_style = Column(Enum(ChatStyle))
    chat_age = Column(Enum(ChatAge))
    answer_length = Column(Enum(AnswerLength))
    has_premium: Mapped[bool] = mapped_column(default=False)