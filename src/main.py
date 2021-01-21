import connection
import telebot
import config
import requests
import session
from services import ids
from services import dateconverter
from services.keyboards import get_main_keyboard,get_clear_keyboard,crearNotas,crearBlogs,crearNotes

lastcommand='lastcommand' #Variable para guardar el ultimo comando ejecutado
lastIdNota='lastIdNota' #Variable para guardar el id de la ultima nota
bot = telebot.TeleBot(config.API_TOKEN) 
#con connecxión a la BD
con=connection.Connection('../database/chatbot_test.db') 
#converter, classe con un conjunto de funcionaledades
converter=dateconverter.Converter()
generadorIds=ids.Ids()

#Te registra como uusuario y te encamina a help
@bot.message_handler(commands=['start'])
def send_welcome(message):
    con=connection.Connection('../database/chatbot_test.db')
    #print(str(today))
    con.insertUsuario(message.from_user.id,message.from_user.first_name,converter.getToday())
    bot.reply_to(message, "Hola con este bot podrás guardar las notas que quieras, ejecuta **__/help__** para saber más",parse_mode='MARKDOWN')
    con.closeConnection()

#Te muestra las instrucciones
@bot.message_handler(commands=['help'])
def send_help(message):
    con=connection.Connection('../database/chatbot_test.db')
    con.insertUsuario(message.from_user.id,message.from_user.first_name,converter.getToday())
    bot.send_message(message.chat.id, config.HELP,parse_mode='MARKDOWN')
    con.closeConnection()

#Crea una nota simple
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

#Crea una nota que tiene contenido media
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

#Crea una nota que está en n blog y tiene contenido media, si el blog no existe, se crea
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

#crea una nota en un blog,si el blog no existe, se crea
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

#crea un nuevo blog
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

#Muestra las notas de un blog
@bot.message_handler(commands=['shownotesfromblog'])
def send_shownotesfromblog(message):
    global lastcommand
    lastcommand='/shownotesfromblog'
    blog=message.text[19:]
    if(blog):
        con=connection.Connection('../database/chatbot_test.db')
        res=con.getNotasFromBlog(message.from_user.id,blog)
        if res != None:
            mensaje=crearNotas(res)
            for m in mensaje:
                bot.send_message(message.chat.id,m,parse_mode='MARKDOWN')
        else:
            bot.send_message(message.chat.id,f'Parece ser que no tienes notas en este blog')
        con.closeConnection()
    else:
        bot.send_message(message.chat.id,f'Parece que tu blog está vacio, intenta escribir **__/shownotesfromblog__** <blog>',parse_mode='MARKDOWN')
    
#Si se manda un documento y se ejecuto un comando anterior como newnotemedia, se edita la ultima nota
@bot.message_handler(content_types=['document'])
def handle_docs_document(message):
    con=connection.Connection('../database/chatbot_test.db')
    global lastcommand
    global lastIdNota
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

#Si se manda un documento y se ejecuto un comando anterior como newnotemedia, se edita la ultima nota
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
        bot.send_message(message.chat.id,f"Consulta tu nota con la fecha {fechaCreacion.year}-{fechaCreacion.month}-{fechaCreacion.day}\n !['Imagen']({media})",parse_mode="MARKDOWN")
    elif(lastcommand=='/newblognotemedia'):
        fechaCreacion= converter.getToday()
        media=converter.getMedia(bot.get_file(message.json['photo'][0]['file_id']))
        aux=generadorIds.getIdBlog(fechaCreacion,message.from_user.id)
        idBlog=con.insertBlog(aux,con.getBlogFromNota(lastIdNota),fechaCreacion,message.from_user.id)
        con.updateMediaNota(media,lastIdNota)
        bot.send_message(message.chat.id,f'Consulta tu nota con la fecha {fechaCreacion.year}-{fechaCreacion.month}-{fechaCreacion.day}\n !["Imagen"]({media})',parse_mode='MARKDOWN')
    con.closeConnection()

#Manjador del teclado
@bot.message_handler(commands=['keyboard'])
def handle_keyboard(message):
    markup = get_main_keyboard()
    bot.send_message(message.chat.id, "Elige una opción: ", reply_markup=markup)

#Manejador de los mensajes
@bot.message_handler(func=lambda message: True)
def send_response(message):
    text = message.text
    # API CLIMA
    con=connection.Connection('../database/chatbot_test.db')
    #Mostrar las notas de hoy
    if text == "Show notes of day":
        ranges=converter.getDateRange()
        res=con.getNotas(ranges[0],ranges[1],message.from_user.id)
        if res != None:
            mensaje=crearNotes(res)
            for m in mensaje:
                bot.send_message(message.chat.id,m)
        else:
            bot.reply_to(message,'Parace ser que no tienes notas hoy.')
    #Mostrar blogs
    elif text == "Show blogs":
        res=con.getBlogs(message.from_user.id)
        if res !=None:
            mensaje=crearBlogs(res)
            for m in mensaje:
                bot.send_message(message.chat.id,m,parse_mode='MARKDOWN')
        else:
            bot.reply_to(message,f'Parece ser que aún no tienes blogs.')
    # QUITAR TECLADO
    elif text == "Hide Keyboard":
        markup = get_clear_keyboard()
        bot.send_message(message.chat.id,"Escribe /keyboard para mostrarlo.", reply_markup=markup)
    else:
        bot.reply_to(message,"No entiendo tu mensaje. Escribe: /help")
    con.closeConnection()


bot.polling()

