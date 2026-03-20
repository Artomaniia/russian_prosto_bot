import json
import random


def get_random_word(words):
    question, answers = random.choice(list(words.items()))
    return question, answers


def load_words(filename):
    with open(filename, "r", encoding="utf-8") as file:
        return json.load(file)


def is_word_correct(user_text, correct_answers):
    user_text = user_text.strip().replace("ё", "е").replace("Ё", "Е")

    for answer in correct_answers:
        answer = answer.strip().replace("ё", "е").replace("Ё", "е")

        if user_text == answer:
            return True
        if user_text == answer[0].upper() + answer[1:]:
            return True

    return False
