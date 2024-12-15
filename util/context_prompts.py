import enum

from database.models import ChatStyle, ChatAge, AnswerLength

CHAT_STYLES = {
    ChatStyle.none: 'Без стиля',
    ChatStyle.story: 'Рассказ',
    ChatStyle.creative: 'Креативный',
    ChatStyle.convincing: 'Убедительный',
    ChatStyle.official: 'Официальный'
}

CHAT_AGE = {
    ChatAge.all: 'Для всех',
    ChatAge.adult: 'Для взрослых',
    ChatAge.teenage: 'Для подростков',
    ChatAge.child: 'Для детей'
}

ANSWER_LENGTH = {
    AnswerLength.none: 'Любой',
    AnswerLength.normal: 'Средний',
    AnswerLength.short: 'Краткий',
    AnswerLength.full: 'Подробный'
}


def get_option_by_name(data: dict[enum.Enum, str], option_name: str) -> enum.Enum:
    inv_map = {v: k for k, v in data.items()}
    return inv_map[option_name]


def create_prompt(text: str, action: str, style: str, age: str, length: str, char: str, form: str) -> str:
    return f"""
        Не используй MarkDown или HTML в своем ответе. Напиши свой ответ исключительно в виде текста без форматирования\n
        Действие: {action}\n
        В стиле: {style}\n
        Для аудитории: {age}\n
        Длина ответа: {length}\n
        Ответ от лица: {char}\n
        В формате: {form}\n
        
        Нужно выполнить действия с параметрами над этим текстом: {text}
    """