import telebot
import config
import requests
from io import BytesIO

bot = telebot.TeleBot(config.API_TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.reply_to(message, "Howdy, how are you doing?")

@bot.message_handler(content_types=['audio', 'document', 'photo', 'sticker', 'video', 'video_note', 'voice', 'location', 'contact'])
def handle_docs_audio(message):
    #print(message)
    file_info = bot.get_file(message.document.file_id)
    path=f'https://api.telegram.org/file/bot{config.API_TOKEN}/{str(file_info.file_path)}'
    file = requests.get(path)
	print(f'file_info: {dir(file_info)}')
	hide=f'Archivo: [{str(file_info.file_path)}]({path})'
    print(f'Hide: {hide}')
    bot.send_message(message.chat.id, hide,parse_mode='MARKDOWN')

@bot.message_handler(func=lambda m: True)
def echo_all(message):
	res=str(message)
	bot.send_message(message.chat.id, res)

bot.polling()
