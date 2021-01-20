from datetime import datetime
class Converter:
    def __init__(self):
        pass
    def getDateFromTimestamp(self,fecha):
            try:
                x = datetime.datetime.fromtimestamp(fecha)
                return x
            except:
                return datetime(1998,3,27)
