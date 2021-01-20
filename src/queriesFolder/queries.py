GET_TABLE='SELECT * from {0};'
GET_USUARIO='SELECT * FROM usuarios WHERE idUsuario={0};'
GET_BLOG='SELECT * FROM blogs WHERE blog LIKE {0};'
GET_BLOGS='SLECET * FROM blogs WHERE idUsuario={0}'
GET_NOTAS='SELECT * FROM notas WHERE fechaCreacion LIKE {0} AND idUsuario={1};'
GET_FILE_NAME='SELECT nombreArchivo FROM notas WHERE idUsuario={0} AND documentId={1};'
GET_NOTAS_OF_BLOG="""SELECT notas.idNota,notas.fechaCreacion,notas.nota,
notas.media,notas.documentId,notas.photoId,notas.caption,notas.nombreArchivo FROM notas,blogs 
where notas.idUsuario={0} AND blogs.idUsuario={0} AND blogs.blog={1} AND notas.idBlog=blogs.idBlog """

INSERT_USUARIO='INSERT INTO usuarios(idUsuario,nombre,fechaIngreso) VALUES ({0},"{1}","{2}");'
INSERT_BLOG='INSERT INTO blogs(idBlog,blog,fechaCreacion,idUsuario) VALUES ("{0}","{1}","{2}",{3});'
INSERT_NOTA='INSERT INTO notas(idNota,fechaCreacion,nota,media,documentId,photoId,caption,nombreArchivo,idUsuario,idBlog) VALUES ("{0}","{1}","{2}","{3}","{4}","{5}","{6}","{7}",{8},"{9}");'

DELETE_NOTA='DELETE FROM notas where idNota={0};'
DELETE_BLOG='DELETE FROM blogs where idBlog={0};'
