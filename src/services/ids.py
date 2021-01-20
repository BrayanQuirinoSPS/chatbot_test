import uuid
from . import dateconverter
class Ids:
    def __init__(self):
        self.converter=dateconverter.Converter()
        self.identificador=str(uuid.uuid4())

    def getId(self,fecha):
        self.identificador+=str(self.converter.getDateFromTimestamp(fecha))
        return self.identificador
    
    def getIdBlog(self,fecha,idUsuario):
        self.identificador+=str(self.converter.getDateFromTimestamp(fecha))
        self.identificador+=str(idUsuario)
        return self.identificador

    
