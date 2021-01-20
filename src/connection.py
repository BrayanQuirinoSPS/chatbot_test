import sqlite3
import queriesFolder import queries

class Connection:
    def __init__(self,database):
        self.connection= sqlite3.connect(database)
        self.cursor=self.connection.cursor()
        #print('Error en la conecxión de la BD.')
    def getTable(self,table):
        self.cursor.execute(queries.GET_TABLES.format(table))
        res=self.cursor.fetchall()
        print(res)
        return (res)
    def insertUsuario(self,idUsuario,nombre,fechaIngreso):
        self.cursor.execute(queries.GET_USUARIO.format(idUsuario))
        if not self.cursor.fetchone():
            self.cursor.execute(queries.INSERT_USUARIO.format(idUsuario,nombre,fechaIgreso))
            self.connection.commit()
    
    def insertBlog(self,idBlog,blog,fechaCreacion,idUsuario):
        self.cursor.execute(queries.GET_BLOG(blog))
        if not self.cursor.fetchone():
            self.cursor.execute(queries.INSERT_BLOG.format(idBlog,blog,fechaCreacion,idUsuario))
            self.connection.commit()
    
    def insertNota(self,idNota,fechaCreacion,nota,media,documentId,photoId,caption,nombreArchivo,idUsuario,idBlog):
        self.cursor.execute(queries.INSERT_NOTA.format(idNota,fechaCreacion,nota,media,documentId,photoId,caption,nombreArchivo,idUsuario,idBlog))
        self.connection.commit()

    def getNotas(self, fechaCreacion,idUsuario):
        self.cursor.execute(queries.GET_NOTAS.format(fechaCreacion,idUsuario))
        res= self.cursor.fetchall()
        if res:
            return res
        return 'No tienes notas en este día'

    def getNotasFromBlog(self, idUsuario,blog):
        self.cursor.execute(queries.GET_NOTAS_FROM_BLOG.format(idUsuario,blog))
        res= self.cursor.fetchall()
        if res:
            return res
        return 'No tienes notas en este blog'
    
    def getBlogs(self,idUsuario):
        self.cursor.execute(queries.GET_BLOGS.format(idUsuario,blog))
        res= self.cursor.fetchall()
        if res:
            return res
        return 'Aún no tienes blogs'
    
    def deleteNota(self,idNote):
        self.cursor.execute(queries.DELETE_NOTA.format(idNote))
        self.connection.commit()

    def deleteBlog(self,idBlog):
        self.cursor.execute(queries.DELETE_BLOG.format(idBlog))
        self.connection.commit()

    def closeConnection(self):
        self.connection.close()


