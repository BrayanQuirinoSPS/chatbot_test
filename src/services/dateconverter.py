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
            lista=[path,file.content]
            return lista
        return 'Sin media'

    def getMediLink(self,file_info,file_id):
        file_info = bot.get_file(message.document.file_id)
        path=f'https://api.telegram.org/file/bot{config.API_TOKEN}/{str(file_info.file_path)}'
        hide=f'Archivo: [{str(file_info.file_path)}]({path})'
        #print(f'Hide: {hide}')
        #bot.send_message(message.chat.id, hide,parse_mode='MARKDOWN')
