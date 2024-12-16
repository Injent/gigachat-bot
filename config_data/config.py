from dataclasses import dataclass
from environs import Env

# Конфиг бота
@dataclass
class TgBotConfig:
    token: str
    payment_token: str


# Конфиг Гигачат
@dataclass
class GigaChatConfig:
    client_secret: str
    client_id: str
    auth_key: str
    base_model: str


# Конфиг БД
@dataclass
class DatabaseConfig:
    database: str


# Класс с конфигами
@dataclass
class Config:
    tg_bot: TgBotConfig
    gigachat: GigaChatConfig
    database: DatabaseConfig


# Чтение переменных
env = Env()
env.read_env()


# Инициализация конфига
config = Config(
    database=DatabaseConfig(
        database=env('DATABASE')
    ),
    tg_bot=TgBotConfig(
        token=env('BOT_TOKEN'),
        payment_token=env('PAYMENT_TOKEN')
    ),
    gigachat=GigaChatConfig(
        client_id=env('CLIENT_ID'),
        client_secret=env('CLIENT_SECRET'),
        auth_key=env('AUTH_KEY'),
        base_model=env('GIGACHAT_MODEL')
    )
)