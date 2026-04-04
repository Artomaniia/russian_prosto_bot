import json

from vkbottle import Keyboard, KeyboardButtonColor, Text


def get_start_keyboard() -> str:
    return (
        Keyboard(one_time=False, inline=False)
        .add(
            Text("help", payload={"cmd": "help"}),
            color=KeyboardButtonColor.SECONDARY,
        )
        .add(
            Text("test", payload={"cmd": "test"}),
            color=KeyboardButtonColor.PRIMARY,
        )
        .get_json()
    )


def get_mode_keyboard() -> str:
    return (
        Keyboard(one_time=False, inline=False)
        .add(Text("Рандом", payload={"cmd": "random"}), color=KeyboardButtonColor.PRIMARY)
        .add(Text("Как в ЕГЭ", payload={"cmd": "ege"}), color=KeyboardButtonColor.SECONDARY)
        .row()
        .add(Text("В начало", payload={"cmd": "to_start"}), color=KeyboardButtonColor.NEGATIVE)
        .get_json()
    )


def get_random_choice_keyboard(options: list[str]) -> str:
    keyboard = Keyboard(one_time=True, inline=False)
    keyboard.add(Text(options[0]), color=KeyboardButtonColor.PRIMARY)
    keyboard.add(Text(options[1]), color=KeyboardButtonColor.SECONDARY)
    return keyboard.get_json()


def get_after_random_keyboard() -> str:
    return (
        Keyboard(one_time=True, inline=False)
        .add(Text("Следующее слово"), color=KeyboardButtonColor.POSITIVE)
        .add(Text("В начало"), color=KeyboardButtonColor.NEGATIVE)
        .get_json()
    )


def get_after_ege_keyboard() -> str:
    return (
        Keyboard(one_time=True, inline=False)
        .add(Text("Следующее задание"), color=KeyboardButtonColor.POSITIVE)
        .add(Text("В начало"), color=KeyboardButtonColor.NEGATIVE)
        .get_json()
    )


def get_empty_keyboard() -> str:
    return json.dumps(
        {
            "one_time": False,
            "inline": False,
            "buttons": [],
        },
        ensure_ascii=False,
    )


def get_main_keyboard() -> str:
    return (
        Keyboard(one_time=False, inline=False)
        .add(Text("start", payload={"cmd": "to_start"}), color=KeyboardButtonColor.POSITIVE)
        .add(Text("help", payload={"cmd": "help"}), color=KeyboardButtonColor.SECONDARY)
        .add(Text("test", payload={"cmd": "test"}), color=KeyboardButtonColor.PRIMARY)
        .get_json()
    )
