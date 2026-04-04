from contextlib import suppress

from vkbottle.bot import BotLabeler, Message
from vkbottle.dispatch.rules.base import CommandRule

from config import state_dispenser
from app.keyboards import *
from app.quiz import *
from app.states import QuizStates
from app.texts import *

labeler = BotLabeler()


async def safe_delete_state(peer_id: int) -> None:
    state = await state_dispenser.get(peer_id)
    if state is not None:
        with suppress(KeyError):
            await state_dispenser.delete(peer_id)


async def _first_name(message: Message) -> str:
    if message.from_id is None:
        return "друг"

    users = await message.ctx_api.users.get([message.from_id])
    if users:
        return users[0].first_name
    return "друг"


async def _go_to_start(message: Message) -> None:
    await safe_delete_state(message.peer_id)
    await state_dispenser.set(message.peer_id, QuizStates.START)
    await message.answer(
        start_message(await _first_name(message)),
        keyboard=get_start_keyboard(),
    )


async def _send_random_question(message: Message) -> None:
    word, answers, options = prepare_random_button_question()
    await state_dispenser.set(
        message.peer_id,
        QuizStates.WAITING_RANDOM_ANSWER,
        answers=answers,
        options=options,
    )
    await message.answer(
        random_question_message(word),
        keyboard=get_random_choice_keyboard(options),
    )


async def _send_ege_question(message: Message) -> None:
    lines, answers = prepare_ege_question()
    await state_dispenser.set(
        message.peer_id,
        QuizStates.WAITING_EGE_ANSWER,
        answers=answers,
    )
    await message.answer(ege_question_message(lines), keyboard=get_empty_keyboard())


@labeler.private_message(CommandRule("start", ["/"], 0))
async def start_command(message: Message) -> None:
    await _go_to_start(message)


@labeler.private_message(text=["начать", "Начать"], state=None)
async def start_text(message: Message) -> None:
    await _go_to_start(message)


@labeler.private_message(CommandRule("help", ["/"], 0))
@labeler.private_message(payload={"cmd": "help"})
async def help_command(message: Message) -> None:
    await state_dispenser.set(message.peer_id, QuizStates.START)
    await message.answer(HELP_COMMAND, keyboard=get_start_keyboard())


@labeler.private_message(CommandRule("test", ["/"], 0))
@labeler.private_message(payload={"cmd": "test"}, state=QuizStates.START)
async def test(message: Message) -> None:
    await safe_delete_state(message.peer_id)
    await state_dispenser.set(message.peer_id, QuizStates.CHOOSING_MODE)
    await message.answer(
        CHOOSE_MODE,
        keyboard=get_mode_keyboard(),
    )


@labeler.private_message(payload={"cmd": "random"}, state=QuizStates.CHOOSING_MODE)
@labeler.private_message(text=["рандом", "Рандом"], state=QuizStates.CHOOSING_MODE)
async def random_mode(message: Message) -> None:
    await safe_delete_state(message.peer_id)
    await _send_random_question(message)


@labeler.private_message(payload={"cmd": "ege"}, state=QuizStates.CHOOSING_MODE)
@labeler.private_message(text=["как в егэ", "Как в ЕГЭ"], state=QuizStates.CHOOSING_MODE)
async def ege_mode(message: Message) -> None:
    await safe_delete_state(message.peer_id)
    await _send_ege_question(message)


@labeler.private_message(payload={"cmd": "to_start"})
@labeler.private_message(text=["В начало", "в начало"])
async def to_start(message: Message) -> None:
    await _go_to_start(message)


@labeler.private_message(text=["Следующее слово", "следующее слово"])
async def continue_random(message: Message) -> None:
    await safe_delete_state(message.peer_id)
    await _send_random_question(message)


@labeler.private_message(text=["Следующее задание", "следующее задание"])
async def continue_ege(message: Message) -> None:
    await safe_delete_state(message.peer_id)
    await _send_ege_question(message)


@labeler.private_message(state=QuizStates.WAITING_RANDOM_ANSWER)
async def process_random_choice(message: Message) -> None:
    user_answer = (message.text or "").strip()
    answers = list(message.state_peer.payload.get("answers", []))
    options = list(message.state_peer.payload.get("options", []))

    if user_answer not in options:
        await message.answer(USE_BUTTONS, keyboard=get_random_choice_keyboard(options))
        return

    await safe_delete_state(message.peer_id)

    if user_answer in answers:
        await message.answer(success_message(answers), keyboard=get_after_random_keyboard())
        return

    await message.answer(fail_message(answers), keyboard=get_after_random_keyboard())


@labeler.private_message(state=QuizStates.WAITING_EGE_ANSWER)
async def process_ege_answer(message: Message) -> None:
    user_answer = parse_ege_answer(message.text or "")
    if user_answer is None:
        await message.answer(USE_DIGITS)
        return

    answers = list(message.state_peer.payload.get("answers", []))
    await safe_delete_state(message.peer_id)

    if user_answer == answers:
        await message.answer(success_message(answers), keyboard=get_after_ege_keyboard())
        return

    await message.answer(fail_message(answers), keyboard=get_after_ege_keyboard())


@labeler.private_message(state=QuizStates.START)
async def start_state_fallback(message: Message) -> None:
    await state_dispenser.set(message.peer_id, QuizStates.START)
    await message.answer(USE_BUTTONS, keyboard=get_start_keyboard())


@labeler.private_message(state=QuizStates.CHOOSING_MODE)
async def choosing_mode_fallback(message: Message) -> None:
    await state_dispenser.set(message.peer_id, QuizStates.CHOOSING_MODE)
    await message.answer(USE_BUTTONS, keyboard=get_mode_keyboard())


@labeler.private_message()
async def handle_unknown_message(message: Message) -> None:
    current_state = await state_dispenser.get(message.peer_id)

    if current_state is not None:
        if current_state.state == QuizStates.START:
            await message.answer(USE_BUTTONS, keyboard=get_main_keyboard())
            return

        if current_state.state == QuizStates.CHOOSING_MODE:
            await message.answer(USE_BUTTONS, keyboard=get_mode_keyboard())
            return

    await safe_delete_state(message.peer_id)
    await state_dispenser.set(message.peer_id, QuizStates.START)
    await message.answer(UNKNOWN_MESSAGE, keyboard=get_main_keyboard())
