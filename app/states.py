from vkbottle import BaseStateGroup


class QuizStates(BaseStateGroup):
    START = "start"
    CHOOSING_MODE = "choosing_mode"
    WAITING_RANDOM_ANSWER = "waiting_random_answer"
    WAITING_EGE_ANSWER = "waiting_ege_answer"
