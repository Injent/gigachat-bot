from aiogram.fsm.state import StatesGroup, State

# Состояния бота
class MenuState(StatesGroup):
    main = State()
    settings = State()


class PromptState(StatesGroup):
    ask = State()
    param_action = State()
    param_character = State()
    param_format = State()
    question = State()


class SettingsState(StatesGroup):
    main = State()
    input_chat_style = State()
    input_answer_length = State()
    input_chat_age = State()