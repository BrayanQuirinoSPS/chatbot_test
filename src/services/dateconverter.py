from datetime import datetime
import sys
sys.path.insert(0, '..')
from src import config
import requests
class Converter:
    def __init__(self):
        pass

    def getDateFromTimestamp(self,fecha):
            try:
                x = datetime.fromtimestamp(fecha)
                return x
            except:
                return datetime.now()

    def getToday(self):
        return datetime.now()

    def getMedia(self,file_info):
        path=f'https://api.telegram.org/file/bot{config.API_TOKEN}/{str(file_info.file_path)}'
        file = requests.get(path)
        if(file.status_code == 200):
            return path
        return 'Sin media'

    def getMediLink(self,file_info,file_id):
        file_info = bot.get_file(message.document.file_id)
        path=f'https://api.telegram.org/file/bot{config.API_TOKEN}/{str(file_info.file_path)}'
        hide=f'Archivo: [{str(file_info.file_path)}]({path})'
        #print(f'Hide: {hide}')
        #bot.send_message(message.chat.id, hide,parse_mode='MARKDOWN')

    def getBlogNote(self,texto):
        cadena=texto[13:]
        lista=cadena.split(';')
        if(len(lista)<=1):
            lista=[None,'Parece que no has escrito de forma correcta el comando. Intenta escribir **__/newblognote__** <blog> **;** <note>']
        else:
            blog=lista[0]
            lista.pop(0)
            nota=";".join(lista)
            lista=[blog,nota]
        return lista


    def getBlogNoteMedia(self,texto):
        cadena=texto[18:]
        lista=[]
        if(len(texto)>18):
            lista=cadena.split(';')
        if(len(lista)==0):
            lista=[None,'Parece que no has escrito de forma correcta el comando. Intenta escribir **__/newblognotemedia__** <blog> **;** <note>\nTambien puedes escribir **__/newblognotemedia__** <blog>;']
        elif(len(lista)==1):
            lista.append('')
        else:
            blog=lista[0]
            lista.pop(0)
            nota=";".join(lista)
            lista=[blog,nota]
        print(lista)
        return lista
            #print(blog)
            #print(nota)

