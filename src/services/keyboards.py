from telebot import types

def get_main_keyboard():
    markup = types.ReplyKeyboardMarkup(row_width=2)
    markup.add(types.KeyboardButton('Show notes of day'))
    markup.add(types.KeyboardButton('Show blogs'))
    markup.add(types.KeyboardButton('Hide Keyboard'))
    return markup

def get_clear_keyboard():
    return types.ReplyKeyboardRemove(selective=False)