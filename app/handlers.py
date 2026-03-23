from telebot import types

from app.keyboards import get_test_keyboard, get_after_answer_keyboard
from app.quiz import *
from app.texts import *
from app.words import is_word_correct


def register_handlers(bot):
    bot.set_my_commands([
        types.BotCommand("start", START_DESCRIPTION),
        types.BotCommand("test", TEST_DESCRIPTION),
        types.BotCommand("help", HELP_DESCRIPTION)
    ])

    bot.set_chat_menu_button(menu_button=types.MenuButtonCommands())

    @bot.message_handler(commands=['start'])
    def start(message):
        chat_id = message.chat.id
        clear_state(chat_id)

        first_name = message.from_user.first_name
        bot.send_message(chat_id, start_message(first_name))

    @bot.message_handler(commands=['help'])
    def start(message):
        chat_id = message.chat.id
        clear_state(chat_id)

        bot.send_message(chat_id, HELP_COMMAND)

    @bot.message_handler(commands=['test'])
    def test(message):
        chat_id = message.chat.id
        clear_state(chat_id)

        bot.send_message(
            chat_id,
            CHOOSE_MODE,
            reply_markup=get_test_keyboard(), parse_mode="HTML"
        )

    @bot.callback_query_handler(func=lambda call: True)
    def process_callback(call):
        chat_id = call.message.chat.id
        first_name = call.from_user.first_name

        bot.answer_callback_query(call.id)
        clear_state(chat_id)

        match call.data:
            case "random":
                question = prepare_random_question(chat_id)
                bot.send_message(chat_id, random_question_message(question), parse_mode="HTML")

            case "continue":
                match get_current_mode(chat_id):
                    case "ege":
                        question = prepare_ege_question(chat_id)
                        bot.send_message(chat_id, ege_question_message(question), parse_mode="HTML")
                    case "random":
                        question = prepare_random_question(chat_id)
                        bot.send_message(chat_id, random_question_message(question), parse_mode="HTML")
                    case _:
                        bot.send_message(chat_id, NO_CHOSEN_MODE, parse_mode="HTML")

            case "to_start":
                bot.send_message(chat_id, start_message(first_name))

            case "ege":
                question = prepare_ege_question(chat_id)
                bot.send_message(chat_id, ege_question_message(question), parse_mode="HTML")

    @bot.message_handler(func=lambda message: has_active_question(message.chat.id))
    def process_user_answer(message):
        chat_id = message.chat.id
        correct_answers = get_current_answers(chat_id)

        match get_current_mode(chat_id):
            case "ege":
                user_answer = parse_ege_answer(message.text)

                if not user_answer:
                    bot.send_message(chat_id, USE_DIGITS, parse_mode="HTML")
                    return

                if user_answer == correct_answers:
                    bot.send_message(
                        chat_id,
                        success_message(correct_answers),
                        reply_markup=get_after_answer_keyboard(), parse_mode="HTML"
                    )
                else:
                    bot.send_message(
                        chat_id,
                        fail_message(correct_answers),
                        reply_markup=get_after_answer_keyboard(), parse_mode="HTML"
                    )

            case "random":
                result = validate_random_answer(message.text)

                if result == "one_word":
                    bot.send_message(chat_id, USE_ONE_WORD, parse_mode="HTML")
                    return

                if result == "cyrillic_only":
                    bot.send_message(chat_id, USE_LETTERS, parse_mode="HTML")
                    return

                if is_word_correct(message.text, correct_answers):
                    bot.send_message(
                        chat_id,
                        success_message(correct_answers),
                        reply_markup=get_after_answer_keyboard(), parse_mode="HTML"
                    )
                else:
                    bot.send_message(
                        chat_id,
                        fail_message(correct_answers),
                        reply_markup=get_after_answer_keyboard(), parse_mode="HTML"
                    )

        clear_state(chat_id)

    @bot.message_handler(func=lambda message: True)
    def handle_unknown_message(message):
        bot.send_message(message.chat.id, UNKNOWN_MESSAGE)
