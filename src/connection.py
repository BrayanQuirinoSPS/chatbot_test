import sqlite3

class Connection:
    def __init__(self,database):
        self.connection= sqlite3.connect(database)
        self.cursor=self.connection.cursor()
        #print('Error en la conecxión de la BD.')
    def getUsuarios(self,query):
        self.cursor.execute('SELECT * from usuarios;')
        res=self.cursor.fetchall()
        print(res)
        return (res)
    def insertUsuario(self,idUsuario,nombre,fechaIgreso):
        self.cursor.execute(f'INSERT INTO usuarios(idUsuario,nombre,fechaIngreso) VALUES ("{idUsuario}","{nombre}","{fechaIgreso}");')
        self.connection.commit()
    def closeConnection(self):
        self.connection.close()


