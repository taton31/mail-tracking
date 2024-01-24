from app import bot, States
from app import get_users, save_users
from app import check_post, parse_post

import time
from telebot import types


users = get_users()


@bot.message_handler(func=lambda message: str(message.chat.id) in users.keys(), commands=['mail'])
def start(message):
    markup = types.InlineKeyboardMarkup()
    markup.row_width = 1
    
    get_status = types.InlineKeyboardButton("Запросить статус", callback_data='get_status')
    markup.add(get_status)

    bot.send_message(message.chat.id, "Что хочешь? \nДля добавления посылки отправь код", reply_markup=markup)
    bot.set_state(message.chat.id, States.mail)




@bot.callback_query_handler(func=lambda call: call.data == 'get_status', state=States.mail)
def send_admin_request(call):
    global users
    users = get_users()
    for product in users[str(call.message.chat.id)]['products'].keys():
        bot.send_message(call.message.chat.id, f"{product}: запрашиваю информацию")
        users[str(call.message.chat.id)]['products'][product]
        try:
            res = parse_post(check_post(users[str(call.message.chat.id)]['products'][product]))
            msg = f'{product}:\n'
            msg += f'Дата:         {res["eventDate"]}\n'
            if 'operation' in res:
                msg += f'Операция: {res["operation"]}\n'
            if 'location' in res:
                msg += f'Локация:   {res["location"]}'
            bot.send_message(call.message.chat.id, msg)
        except:
            bot.send_message(call.message.chat.id, f"{product}:\nПроизошла ошибка при запросе\nПопробуйте позже")
    try:
        bot.answer_callback_query(call.id)
    except:
        pass






@bot.message_handler(func=lambda message: str(message.chat.id) in users.keys(), state=States.mail)
def start(message):
    bot.send_message(message.chat.id, "Введи название")
    
    bot.register_next_step_handler_by_chat_id(message.chat.id, name_to_product, (message.text, ))





def name_to_product(message, track):
    global users
    users = get_users()
    users[str(message.chat.id)]['products'][message.text] = track[0]
    save_users(users)
    bot.send_message(message.chat.id, "Сохранено")


