from telebot import types
import datetime

#Crea los botones
def get_main_keyboard():
    markup = types.ReplyKeyboardMarkup(row_width=2)
    markup.add(types.KeyboardButton('Show notes of day'))
    markup.add(types.KeyboardButton('Show blogs'))
    markup.add(types.KeyboardButton('Hide Keyboard'))
    return markup

#Borra el teclado
def get_clear_keyboard():
    return types.ReplyKeyboardRemove(selective=False)

# Setea el resultado de la consulta getNotasFromBlog a la bd en mensajes menores a 2999 bytes
def crearNotas(lista):
    mensaje='Notas:\n'
    line=''
    mensajes=[]
    for tupla in lista:
        if(tupla[3]!='' and tupla[3]!='Sin media'):
            line=f'fecha:{getFecha(tupla[1])}| nota:{tupla[2]}| media:[Download file]({tupla[3]})\n'
            if acortador(mensaje,line):
                mensajes.append(mensaje)
                mensaje=''
        else:
            line=f'fecha:{getFecha(tupla[1])}| nota:{tupla[2]}\n'
            if acortador(mensaje,line):
                mensajes.append(mensaje)
                mensaje=''
        mensaje+=line
        #print(mensajes)
    mensajes.append(mensaje)
    return mensajes

#Setea el resultado de la consulta getNotas de hoy, en mensajes menores a 2999 bytes
def crearNotes(lista):
    mensaje='Notas:\n'
    line=''
    mensajes=[]
    for tupla in lista:
        if(tupla[2]!='' and tupla[2]!='Sin media'):
            line=f'fecha:{getFecha(tupla[0])}| nota:{tupla[1]}| media:[Download file]({tupla[2]})\n'
            if acortador(mensaje,line):
                mensajes.append(mensaje)
                mensaje=''
        else:
            line=f'fecha:{getFecha(tupla[0])}| nota:{tupla[1]}\n'
            if acortador(mensaje,line):
                mensajes.append(mensaje)
                mensaje=''
        mensaje+=line
    mensajes.append(mensaje)
    return mensajes

#Setea la consulta getBlogs en mensajes menores a 2999
def crearBlogs(lista):
    mensaje='Blogs:\n'
    line=''
    mensajes=[]
    for tupla in lista:
        line=f'Blog: {tupla[0]}\n'
        if acortador(mensaje,line):
            mensajes.append(mensaje)
            mensaje=''
        mensaje+=line
    mensajes.append(mensaje)
    return mensajes

#Obtiene la fecha en string obtenida de la bd
def getFecha(fecha):
    date=fecha.split()
    x=datetime.datetime.strptime(date[0],'%Y-%m-%d')
    return f'{x.year}-{x.month}-{x.day}'

#Indica si un mensaje sobrepasa los 2999 bytes
def acortador(ori,suma):
    if len(ori+suma)>=2999:
        return True
    return False
