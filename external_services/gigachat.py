import uuid
from typing import Final
import requests
import json

from gigachat import GigaChat

from config_data.config import config


SCOPE: Final[str] = 'GIGACHAT_API_PERS'


gigachat = GigaChat(
    credentials=config.gigachat.auth_key,
    verify_ssl_certs=False,
    scope=SCOPE
)

async def answer_gigachat(text: str) -> str:
    response = gigachat.chat(text)
    return response.choices[0].message.content