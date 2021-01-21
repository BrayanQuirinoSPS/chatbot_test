from telebot import types
import datetime

def get_main_keyboard():
    markup = types.ReplyKeyboardMarkup(row_width=2)
    markup.add(types.KeyboardButton('Show notes of day'))
    markup.add(types.KeyboardButton('Show blogs'))
    markup.add(types.KeyboardButton('Hide Keyboard'))
    return markup

def get_clear_keyboard():
    return types.ReplyKeyboardRemove(selective=False)

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
    #('db7d719d-b8b7-4f05-bfc8-14a9fe77bb9c2021-01-21 04:32:192021-01-21 04:33:27.50108415379540352021-01-21 04:33:272021-01-21 04:33:50.90871515379540352021-01-21 04:34:20', '2021-01-21 04:34:20.176895', '', 'https://api.telegram.org/file/bot1580518953:AAFf_Kb9i1KSGwowFQNGteVKkH8_qm56_RY/documents/file_90.jpg', 'Sin documentId', 'Sin photoId', 'Sin caption', 'Sin nombreArchivo')
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
    #print(mensajes)
    mensajes.append(mensaje)
    return mensajes

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

def getFecha(fecha):
    date=fecha.split()
    x=datetime.datetime.strptime(date[0],'%Y-%m-%d')
    return f'{x.year}-{x.month}-{x.day}'

def acortador(ori,suma):
    if len(ori+suma)>=2999:
        return True
    return False
