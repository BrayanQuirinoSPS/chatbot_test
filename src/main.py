import connection
import uuid

path='../database/chatbot_test.db'
query1='SELECT * from usuarios;'
query2='INSERT INTO usuarios(idUsuario,nombre,fechaIngreso) VALUES ("ccc-ddd-eee","Eduardo","2021-01-19");'
con= connection.Connection(path)
con.getUsuarios(query1)
con.insertUsuario(str(uuid.uuid4()),'Eduardo','2021-01-19')
con.closeConnection()
