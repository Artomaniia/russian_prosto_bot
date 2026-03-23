import random
import re
import unicodedata

from app.common import user_state, TRUE_WORDS, user_mode, FALSE_WORDS
from app.words import get_random_word


def get_current_answers(chat_id):
    return user_state.get(chat_id)


def get_current_mode(chat_id):
    return user_mode.get(chat_id)


def clear_state(chat_id):
    user_state.pop(chat_id, None)


def has_active_question(chat_id):
    return chat_id in user_state


def prepare_random_question(chat_id):
    question, answers = get_random_word(TRUE_WORDS)
    user_state[chat_id] = answers
    user_mode[chat_id] = "random"
    return question


def prepare_ege_question(chat_id):
    available_words = list(set(TRUE_WORDS.keys()) & set(FALSE_WORDS.keys()))
    selected_words = random.sample(available_words, 5)

    correct_indexes = sorted(random.sample(range(1, 6), random.randint(2, 4)))
    answers = [str(index) for index in correct_indexes]

    lines = []
    for index, word in enumerate(selected_words, start=1):
        if index in correct_indexes:
            shown_word = random.choice(TRUE_WORDS[word])
        else:
            shown_word = random.choice(FALSE_WORDS[word])

        lines.append(f"{index}) {shown_word}")

    user_state[chat_id] = answers
    user_mode[chat_id] = "ege"

    return lines


def parse_ege_answer(text):
    if not text.replace(" ", "").isdigit():
        return False

    return sorted(set(re.findall(r"[1-5]", text)))


def validate_random_answer(text):
   text = text.strip()

   if len(text.split()) != 1:
       return "one_word"

   for char in text:
       try:
           if 'CYRILLIC' not in unicodedata.name(char).upper():
               return "cyrillic_only"

       except ValueError:
           return "cyrillic_only"

   return "ok"
