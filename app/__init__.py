import telebot
from telebot.handler_backends import State, StatesGroup
from telebot import custom_filters

from telebot.storage import StateMemoryStorage


state_storage = StateMemoryStorage() 

class States(StatesGroup):
    new_user = State() 
    admin = State()
    mail = State()


bot = telebot.TeleBot('6918830690:AAFlkINc_QPnJfQE0cnILqg2ey5i2PbBp-c', state_storage=state_storage)

from mail_tracking import check_post, parse_post
from db.files import get_admins, save_admins, get_users, save_users, get_request_users, save_request_users


from app.handlers import new_user, admin, config, mail, error

bot.add_custom_filter(custom_filters.StateFilter(bot))