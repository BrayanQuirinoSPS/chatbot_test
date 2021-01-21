import connection
import telebot
import config
import requests
import session
from services import ids
from services import dateconverter
from io import BytesIO

lastcommand='lastcommand'
lastIdNota='lastIdNota'
bot = telebot.TeleBot(config.API_TOKEN)
con=connection.Connection('../database/chatbot_test.db')
converter=dateconverter.Converter()
generadorIds=ids.Ids()

@bot.message_handler(commands=['start'])
def send_welcome(message):
    con=connection.Connection('../database/chatbot_test.db')
    #print(str(today))
    con.insertUsuario(message.from_user.id,message.from_user.first_name,converter.getToday())
    bot.reply_to(message, "Hola con este bot podrás guardar las notas que quieras, ejecuta **__/help__** para saber más",parse_mode='MARKDOWN')
    con.closeConnection()
@bot.message_handler(commands=['help'])
def send_help(message):
    con=connection.Connection('../database/chatbot_test.db')
    con.insertUsuario(message.from_user.id,message.from_user.first_name,converter.getToday())
    bot.send_message(message.chat.id, config.HELP,parse_mode='MARKDOWN')
    con.closeConnection()

@bot.message_handler(commands=['simplenote'])
def send_simplenote(message):
    global lastcommand
    lastcommand='/simplenote'
    nota=message.text[11:]
    if(nota):
        con=connection.Connection('../database/chatbot_test.db')
        idNota=generadorIds.getId(message.date)
        fechaCreacion=converter.getToday()
        con.insertNota(idNota,fechaCreacion,nota,message.from_user.id)
        bot.send_message(message.chat.id,f'Nota guardada con fecha {fechaCreacion.year}-{fechaCreacion.month}-{fechaCreacion.day}')
        con.closeConnection()
    else:
        bot.send_message(message.chat.id,f'Parece que tu nota está vacia, intenta escribir **__/simplenote__** <nota>',parse_mode='MARKDOWN')

@bot.message_handler(commands=['newnotemedia'])
def send_newnotemedia(message):
    con=connection.Connection('../database/chatbot_test.db')
    global lastcommand
    global lastIdNota
    #print(lastcommand)
    lastcommand='/newnotemedia'
    lastIdNota = generadorIds.getId(message.date)
    con.insertNota(lastIdNota,converter.getToday(),message.text[12:],message.from_user.id)
    bot.send_message(message.chat.id,'Envia tu documento')
    con.closeConnection()


@bot.message_handler(commands=['newblognotemedia'])
def send_newblognotemedia(message):
    global lastcommand
    global lastIdNota
    #print(lastcommand)
    lastcommand='/newblognotemedia'
    blogNote=converter.getBlogNoteMedia(message.text)
    if(blogNote[0]==None):
        bot.send_message(message.chat.id,blogNote[1],parse_mode='MARKDOWN')
    else:
        con=connection.Connection('../database/chatbot_test.db')
        lastIdNota = generadorIds.getId(message.date)
        con.insertBlogNota(lastIdNota,converter.getToday(),blogNote[1],message.from_user.id,blogNote[0])
        bot.send_message(message.chat.id,'Envia tu documento')
        con.closeConnection()

@bot.message_handler(commands=['newblognote'])
def send_newnblognote(message):
    global lastcommand
    lastcommand='/newblognote'
    blogNote=converter.getBlogNote(message.text)
    if(blogNote[0]==None):
        bot.send_message(message.chat.id,blogNote[1],parse_mode='MARKDOWN')
    else:
        con=connection.Connection('../database/chatbot_test.db')
        fechaCreacion= converter.getToday()
        aux=generadorIds.getIdBlog(fechaCreacion,message.from_user.id)
        idBlog=con.insertBlog(aux,blogNote[0],fechaCreacion,message.from_user.id)
        print(idBlog)
        idNota=generadorIds.getId(message.date)
        con.insertBlogNota(idNota,fechaCreacion,blogNote[1],message.from_user.id,idBlog)
        bot.send_message(message.chat.id,f'Nota guardada con fecha {fechaCreacion.year}-{fechaCreacion.month}-{fechaCreacion.day} en el blog "{blogNote[0]}"')
        con.closeConnection()

@bot.message_handler(commands=['newblog'])
def send_newblog(message):
    global lastcommand
    lastcommand='/newblog'
    blog=message.text[8:]
    if(blog):
        con=connection.Connection('../database/chatbot_test.db')
        fechaCreacion= converter.getToday()
        idBlog=generadorIds.getIdBlog(fechaCreacion,message.from_user.id)
        idBlog=con.insertBlog(idBlog,blog,fechaCreacion,message.from_user.id)
        bot.send_message(message.chat.id,f'El blog "{blog}" fue creado')
        con.closeConnection()
    else:
        bot.send_message(message.chat.id,f'Parece que tu blog está vacio, intenta escribir **__/newblog__** <blog>',parse_mode='MARKDOWN')
    

@bot.message_handler(content_types=['document'])
def handle_docs_document(message):
    con=connection.Connection('../database/chatbot_test.db')
    global lastcommand
    global lastIdNota
    #print(f'LastIdNota: {lastIdNota}')
    if (lastcommand == '/newnotemedia'):
        fechaCreacion=converter.getToday()
        media=converter.getMedia(bot.get_file(message.document.file_id))
        con.updateMediaNota(media,lastIdNota)
        bot.send_message(message.chat.id,f'Consulta tu nota con la fecha {fechaCreacion.year}-{fechaCreacion.month}-{fechaCreacion.day}\n[Download file]({media})',parse_mode='MARKDOWN')
    elif(lastcommand == '/newblognotemedia'):
        fechaCreacion= converter.getToday()
        media=converter.getMedia(bot.get_file(message.document.file_id))
        aux=generadorIds.getIdBlog(fechaCreacion,message.from_user.id)
        idBlog=con.insertBlog(aux,con.getBlogFromNota(lastIdNota),fechaCreacion,message.from_user.id)
        con.updateMediaNota(media,lastIdNota)
        bot.send_message(message.chat.id,f'Consulta tu nota del blog "{con.getBlogFromNota(lastIdNota)}"con la fecha {fechaCreacion.year}-{fechaCreacion.month}-{fechaCreacion.day}\n[Download file]({media})',parse_mode='MARKDOWN')
    con.closeConnection()

@bot.message_handler(content_types=['photo'])
def handle_docs_document(message):
    con=connection.Connection('../database/chatbot_test.db')
    global lastcommand
    global lastIdNota
    if (lastcommand == '/newnotemedia'):
        fechaCreacion=converter.getToday()
        media=converter.getMedia(bot.get_file(message.json.photo[0].file_id))
        con.updateMediaNota(media,lastIdNota,message.caption)
        bot.send_message(message.chat.id,f'Consulta tu nota con la fecha {fechaCreacion.year}-{fechaCreacion.month}-{fechaCreacion.day}\n![✔]({media})',parse_mode='MARKDOWN')
    con.closeConnection()
    

#@bot.message_handler(content_types=['audio', 'document', 'photo', 'sticker', 'video', 'video_note', 'voice', 'location', 'contact'])
#def handle_docs_audio(message):
#    #print(message)
#    file_info = bot.get_file(message.document.file_id)
#    path=f'https://api.telegram.org/file/bot{config.API_TOKEN}/{str(file_info.file_path)}'
#    file = requests.get(path)
#    print(f'file_info: {dir(file_info)}')
#    hide=f'Archivo: [{str(file_info.file_path)}]({path})'
#    print(f'Hide: {hide}')
#    bot.send_message(message.chat.id, hide,parse_mode='MARKDOWN')

@bot.message_handler(func=lambda m: True)
def echo_all(message):
	res=str(message)
	bot.send_message(message.chat.id, res)

bot.polling()
