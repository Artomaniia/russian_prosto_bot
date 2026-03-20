from app.words import load_words
from config import TRUE_WORDS_FILE, FALSE_WORDS_FILE

user_state = {}
user_mode = {}
TRUE_WORDS = load_words(TRUE_WORDS_FILE)
FALSE_WORDS = load_words(FALSE_WORDS_FILE)
