import random
import re

from config import FALSE_WORDS_FILE, TRUE_WORDS_FILE
from app.words import WordMap, load_words

TRUE_WORDS: WordMap = load_words(TRUE_WORDS_FILE)
FALSE_WORDS: WordMap = load_words(FALSE_WORDS_FILE)


def prepare_random_button_question() -> tuple[str, list[str], list[str]]:
    available_words = list(set(TRUE_WORDS.keys()) & set(FALSE_WORDS.keys()))
    if not available_words:
        raise ValueError("В словарях нет общих слов для режима 'Рандом'.")

    word = random.choice(available_words)

    correct_answer = random.choice(TRUE_WORDS[word])

    wrong_candidates = [item for item in FALSE_WORDS[word] if item != correct_answer]
    if not wrong_candidates:
        raise ValueError(f"Для слова '{word}' нет неверного варианта в false_words.json.")

    wrong_answer = random.choice(wrong_candidates)

    options = [correct_answer, wrong_answer]
    random.shuffle(options)

    return word, [correct_answer], options


def prepare_ege_question() -> tuple[list[str], list[str]]:
    available_words = list(set(TRUE_WORDS.keys()) & set(FALSE_WORDS.keys()))
    selected_words = random.sample(available_words, 5)
    correct_indexes = sorted(random.sample(range(1, 6), random.randint(2, 4)))
    answers = [str(index) for index in correct_indexes]
    lines: list[str] = []

    for index, word in enumerate(selected_words, start=1):
        variants = TRUE_WORDS if index in correct_indexes else FALSE_WORDS
        shown_word = random.choice(variants[word])
        lines.append(f"{index}) {shown_word}")

    return lines, answers


def parse_ege_answer(text: str) -> list[str] | None:
    compact_text = text.replace(" ", "")
    if not compact_text.isdigit():
        return None
    return sorted(set(re.findall(r"[1-5]", text)))
