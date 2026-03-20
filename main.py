import telebot

from app.handlers import register_handlers
from config import API_KEY

bot = telebot.TeleBot(API_KEY)

register_handlers(bot)
bot.infinity_polling()
