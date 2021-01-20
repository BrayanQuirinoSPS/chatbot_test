import uuid
import dateConverter
class Ids:
    def __init__(self):
        self.converter=dateConverter.Converter()
        self.identificador=str(uuid.uuid4())

    def getId(fecha):
        self.identificador+=str(self.converter.getDateFromTimestamp(fecha))
        return self.identificador

    