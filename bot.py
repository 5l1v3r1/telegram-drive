import config
import os
import telebot
from telebot import types

bot = telebot.TeleBot(config.token)
# Path to your folder
path = '.\{}'.format(config.default_path)


def check_id(message):
    return message.from_user.id in config.accepted_users


def generate_keyboard():
    files = types.InlineKeyboardMarkup()
    if path != '.\{}'.format(config.default_path):
        files.add(types.InlineKeyboardButton(text='Back', callback_data='Back'))
    for file in os.listdir(path):
        if os.path.isdir(os.path.join(path, file)):
            files.add(types.InlineKeyboardButton(text=file+'/', callback_data=file))
        else:
            files.add(types.InlineKeyboardButton(text=file, callback_data=file))
    files.add(types.InlineKeyboardButton(text='Done', callback_data='Done'))
    return files


@bot.message_handler(commands=['start', 'help'])
def start(message):
    if check_id(message):
        bot.send_message(message.chat.id, config.help_text,
                         parse_mode='Markdown')
    else:
        bot.send_message(message.chat.id, config.errors['no_access'])


@bot.message_handler(commands=['file_list'])
def show_files(message):
    if not check_id(message):
        bot.send_message(message.chat.id, config.errors['no_access'])
        return

    bot.send_message(
        message.chat.id, 'Choose one of the files or directories', reply_markup=generate_keyboard())


@bot.callback_query_handler(func=lambda call: call.data in os.listdir(path) or call.data in ['Done', 'Back'])
def send_file(call):
    global path
    new_path = os.path.join(path, call.data)

    if call.data == 'Done':
        bot.delete_message(call.from_user.id, call.message.message_id)
        bot.send_message(call.from_user.id, 'Nice!')
        path = '.\{}'.format(config.default_path)

    elif call.data == 'Back':
        path = os.path.split(path)[0]
        bot.delete_message(call.from_user.id, call.message.message_id)
        bot.send_message(
            call.from_user.id, 'Choose one of the files or directories', reply_markup=generate_keyboard())

    elif os.path.isdir(new_path):
        path = new_path
        bot.delete_message(call.from_user.id, call.message.message_id)
        bot.send_message(
            call.from_user.id, 'Choose one of the files or directories', reply_markup=generate_keyboard())

    elif os.stat(new_path).st_size == 0:
        bot.send_message(call.from_user.id, config.errors['empty_file'])

    else:
        with open(new_path, 'rb') as file:
            bot.send_document(call.from_user.id, file)


if __name__ == '__main__':
    bot.polling(none_stop=True)
