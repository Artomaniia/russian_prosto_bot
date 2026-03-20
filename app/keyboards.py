from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_test_keyboard():
    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton("Рандом", callback_data="random"),
        InlineKeyboardButton("Как в ЕГЭ", callback_data="ege")
    )
    return keyboard


def get_after_answer_keyboard():
    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton("Продолжить", callback_data="continue_random"),
        InlineKeyboardButton("В начало", callback_data="to_start")
    )
    return keyboard
