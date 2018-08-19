# Import file with main variables
import config

import os
import telebot
from telebot import types

bot = telebot.TeleBot(config.token)
# Path to our folder and files
path = './{}/'.format(config.default_path)

# Answering to /start and /help commands
@bot.message_handler(commands=['start', 'help'])
def start_menu(message):
    bot.send_chat_action(message.chat.id, 'typing')
    # Verifying user. If there is no such user in array of accepted users, return
    if not checkID(message):
        bot.send_message(message.chat.id, config.errors['no_access'])
        return

    bot.send_message(message.chat.id, config.help_text, parse_mode='Markdown')

# Send list of files
@bot.message_handler(commands=['file_list'])
def request_file_list(message):
    # Verifying user
    if not checkID(message):
        bot.send_message(message.chat.id, config.errors['no_access'])
        return

    # Creating keyboard markup
    # Adding buttons with names of files
    files_list = types.ReplyKeyboardMarkup()
    for f in os.listdir(path):
        list_item = types.KeyboardButton(text=f)
        files_list.add(list_item)
    # Button "Done"
    # We need this button to be able to download more than one file
    files_list.add('Done')

    bot.send_message(message.chat.id, 'Choose one of the files or directories', reply_markup=files_list)

# Reset all
# Set path to default and removing keyboard
@bot.message_handler(func=lambda message: message.text == 'Done')
def reset_all(message):
    global path
    path = './{}/'.format(config.default_path)
    remove_list = types.ReplyKeyboardRemove()
    bot.send_message(message.chat.id, 'Nice', reply_markup=remove_list)

# If user sends file name (or button is pressed)
@bot.message_handler(content_types=['text'], func=lambda message: message.text in os.listdir(path))
def send_file(message):
    global path
    # Verifying user
    if not checkID(message):
        bot.send_message(message.chat.id, config.errors['no_access'])
        return

    # Creating new path with text of message
    file_path = path + message.text

    # Checking if it is a folder
    if os.path.isdir(path + message.text):
        # Adding folder name to path
        path += message.text
        # Creating new keyboard (because we changed path)
        files_list = types.ReplyKeyboardMarkup()
        # Button "Back"
        files_list.add('↑ Back')
        for f in os.listdir(path):
            list_item = types.KeyboardButton(text=f)
            files_list.add(list_item)
        files_list.add('Done')

        bot.send_message(message.chat.id, 'Choose one of the files or directories', reply_markup=files_list)
        # We have to add / in the end of path
        path += '/'
        return

    # If it is a file:
    # We can't send empty files in Telegram, so we have to check the file
    if is_empty(file_path):
        bot.send_message(message.chat.id, config.errors['empty_file'])
        return

    # Open and send the file
    requested_file = open(file_path, 'rb')
    bot.send_document(message.chat.id, requested_file)

# Exit a folder
@bot.message_handler(func=lambda message: message.text == '↑ Back')
def prevoius_folder(message):
    global path
    splited_path = path.split('/')

    if path != './{}/'.format(config.default_path):
        for elem in splited_path:
            if elem == '':
                splited_path.remove(elem)
        # Removing last folder name from path
        path = ''
        for i in range(len(splited_path) - 1):
            path += splited_path[i]
            path += '/'

        # Creating new keyboard
        files_list = types.ReplyKeyboardMarkup()
        if path != './{}/'.format(config.default_path):
            files_list.add('↑ Back')

        for f in os.listdir(path):
            list_item = types.KeyboardButton(text=f)
            files_list.add(list_item)
        files_list.add('Done')

        bot.send_message(message.chat.id, 'Choose one of the files or directories', reply_markup=files_list)
    else:
        remove_list = types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id, 'Oops', reply_markup=remove_list)

# Answering to text
@bot.message_handler(content_types=['text'])
def plain_text(message):
    bot.send_message(message.chat.id, config.errors['plain_text'])

# Functions
def is_empty(filename):
    if os.stat(filename).st_size == 0:
        return True
    else:
        return False

def checkID(message):
    if message.from_user.id not in config.accepted_users:
        return False
    else:
        return True

if __name__ == '__main__':
    bot.polling(none_stop=True)
