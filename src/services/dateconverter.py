from datetime import datetime
from datetime import timedelta
import sys
sys.path.insert(0, '..')
from src import config
import requests
class Converter:
    def __init__(self):
        pass
    
    #Retorna una fecha dado un timestamp
    def getDateFromTimestamp(self,fecha):
            try:
                x = datetime.fromtimestamp(fecha)
                return x
            except:
                return datetime.now()

    #Retorna la fecha del dia actual
    def getToday(self):
        return datetime.now()

    #Retorna la fecha actual y la fecha menos un día
    def getDateRange(self):
        x = datetime.now()
        date_before = x + timedelta(-1)
        return [date_before,x]

    #Retorna el path para descargar el archivo
    def getMedia(self,file_info):
        path=f'https://api.telegram.org/file/bot{config.API_TOKEN}/{str(file_info.file_path)}'
        file = requests.get(path)
        if(file.status_code == 200):
            return path
        return 'Sin media'

    #Retorna una lista con el blog y nota 
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

    #Retorna una lista con el blog y nota(puede no estar)
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
        return lista


