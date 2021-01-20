import connection
import telebot
import config
import requests
import session
import datetime
from services import ids
from services import dateconverter
from io import BytesIO

lastcommand=''
today = datetime.datetime.now()
bot = telebot.TeleBot(config.API_TOKEN)
con=connection.Connection('../database/chatbot_test.db')
converter=dateconverter.Converter()
generadorIds=ids.Ids()

@bot.message_handler(commands=['start'])
def send_welcome(message):
    con=connection.Connection('../database/chatbot_test.db')
    #print(str(today))
    con.insertUsuario(message.from_user.id,message.from_user.first_name,str(today))
    bot.reply_to(message, "Hola con este bot podrás guardar las notas que quieras, ejecuta **__/help__** para saber más",parse_mode='MARKDOWN')
    con.closeConnection()
@bot.message_handler(commands=['help'])
def send_help(message):
    con=connection.Connection('../database/chatbot_test.db')
    con.insertUsuario(message.from_user.id,message.from_user.first_name,str(today))
    bot.send_message(message.chat.id, config.HELP,parse_mode='MARKDOWN')
    con.closeConnection()

@bot.message_handler(commands=['simplenote'])
def send_simplenote(message):
    con=connection.Connection('../database/chatbot_test.db')
    lastcommand='/simplenote'
    #print(dir(generadorIds))
    idNota=generadorIds.getId(message.date)
    fechaCreacion=converter.getDateFromTimestamp(message.date)
    nota=message.text[12:]
    con.insertNota(idNota,str(fechaCreacion),nota,None,None,None,None,None,message.from_user.id,None)
    bot.send_message(message.chat.id,f'Nota guardada con fecha {fechaCreacion.year}-{fechaCreacion.month}-{fechaCreacion.day}')
    con.closeConnection()

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
