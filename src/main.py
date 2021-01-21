import connection
import telebot
import config
import requests
import session
from services import ids
from services import dateconverter
from io import BytesIO
from services.keyboards import get_main_keyboard,get_clear_keyboard

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
        #print(idBlog)
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

@bot.message_handler(commands=['shownotesfromblog'])
def send_shownotesfromblog(message):
    global lastcommand
    lastcommand='/shownotesfromblog'
    blog=message.text[19:]
    if(blog):
        con=connection.Connection('../database/chatbot_test.db')
        res=con.getNotasFromBlog(message.from_user.id,blog)
        if res:
            #print(res)
            bot.send_message(message.chat.id,f'El notas "{res}" fue creado')
        else:
            bot.send_message(message.chat.id,f'Problema')
        con.closeConnection()
    else:
        bot.send_message(message.chat.id,f'Parece que tu blog está vacio, intenta escribir **__/shownotesfromblog__** <blog>',parse_mode='MARKDOWN')
    

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
    #print(message.json['photo'][0]['file_id'])
    if (lastcommand == '/newnotemedia'):
        fechaCreacion=converter.getToday()
        media=converter.getMedia(bot.get_file(message.json['photo'][0]['file_id']))
        con.updateMediaNota(media,lastIdNota,message.caption)
        #print(f'Consulta tu nota con la fecha {fechaCreacion.year}-{fechaCreacion.month}-{fechaCreacion.day}\n![✔]({media})')
        bot.send_message(message.chat.id,f"Consulta tu nota con la fecha {fechaCreacion.year}-{fechaCreacion.month}-{fechaCreacion.day}\n !['Imagen']({media})",parse_mode="MARKDOWN")
    elif(lastcommand=='/newblognotemedia'):
        fechaCreacion= converter.getToday()
        media=converter.getMedia(bot.get_file(message.json['photo'][0]['file_id']))
        aux=generadorIds.getIdBlog(fechaCreacion,message.from_user.id)
        idBlog=con.insertBlog(aux,con.getBlogFromNota(lastIdNota),fechaCreacion,message.from_user.id)
        con.updateMediaNota(media,lastIdNota)
        bot.send_message(message.chat.id,f'Consulta tu nota con la fecha {fechaCreacion.year}-{fechaCreacion.month}-{fechaCreacion.day}\n !["Imagen"]({media})',parse_mode='MARKDOWN')
    con.closeConnection()


@bot.message_handler(commands=['keyboard'])
def handle_keyboard(message):
    markup = get_main_keyboard()
    bot.send_message(message.chat.id, "Elige una opción: ", reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def send_response(message):
    text = message.text
    # API CLIMA
    con=connection.Connection('../database/chatbot_test.db')
    if text == "Show notes of day":
        ranges=converter.getDateRange()
        res=con.getNotas(ranges[0],ranges[1],message.from_user.id)
        if res:
            print(res)
            bot.reply_to(message,f'Res: {res}',parse_mode="MARKDOWN")
        else:
            bot.reply_to(message,f'Problema',parse_mode="MARKDOWN")
    elif text == "Show blogs":
        res=con.getBlogs(message.from_user.id)
        if res:
            print(res)
            bot.reply_to(message,f'Res: {res}',parse_mode="MARKDOWN")
        else:
            bot.reply_to(message,f'Problema',parse_mode="MARKDOWN")
    # QUITAR TECLADO
    elif text == "Hide Keyboard":
        markup = get_clear_keyboard()
        bot.send_message(message.chat.id,"Escribe /teclado para mostrarlo.", reply_markup=markup)
    else:
        bot.reply_to(message,"No entiendo tu mensaje. Escribe: /help")
    con.closeConnection()



bot.polling()

