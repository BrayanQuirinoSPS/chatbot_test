import connection
import telebot
import config
import requests
import session
import datetime
from services import ids, dateConverter
from io import BytesIO

lastcommand=''
today = datetime.datetime.now()
bot = telebot.TeleBot(config.API_TOKEN)
con=connection.Connection('../database/chatbot_test.db')
converter=dateConverter.Converter()
ids=ids.Ids()

@bot.message_handler(commands=['start'])
def send_welcome(message):
    con=connection.Connection('../database/chatbot_test.db')
    con.insertUsuario(message.from_user.id,message.from_user.first_name,str(today))
	bot.reply_to(message, "Hola con este bot podrás guardar las notas que quieras, ejecuta **_/help_** para saber más",parse_mode='MARKDOWN')

@bot.message_handler(commands=['help'])
def send_welcome(message):
    con.insertUsuario(message.from_user.id,message.from_user.first_name,str(today))
	bot.send_message(message.chat.id, config.HELP,parse_mode='MARKDOWN')

@bot.message_handler(commands=['close'])
def send_welcome(message):
    con.closeConnection()
	bot.send_message(message.chat.id, 'Conecxión cerrada')

@bot.message_handler(commands=['simplenote'])
def send_welcome(message):
    lastcommand='/simplenote'
    idNota=ids.getId(message.date)
    fechaCreacion=converter.getDateFromTimestamp(message.date)
    nota=meesage.text[9:]
    con.insertNota(idNota,fechaCreacion,nota,None,None,None,None,None,message.from_user.id,None)
	bot.send_message(message.chat.id, ,parse_mode='MARKDOWN')

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
