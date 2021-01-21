GET_TABLE='SELECT * from {0};'
GET_USUARIO='SELECT * FROM usuarios WHERE idUsuario={0};'
GET_BLOG='SELECT * FROM blogs WHERE blog = "{0}" and idUsuario={1};'
GET_BLOGS='SLECET blog FROM blogs WHERE idUsuario={0}'
GET_NOTAS='SELECT * FROM notas WHERE fechaCreacion > "{0}" fechaCreacion <="{1}" AND idUsuario={2};'
GET_FILE_NAME='SELECT nombreArchivo FROM notas WHERE idUsuario={0} AND documentId={1};'
GET_BLOG_FROM_NOTA='SELECT idBlog FROM notas where idNota="{0}"'
GET_NOTAS_FROM_BLOG="""SELECT notas.idNota,notas.fechaCreacion,notas.nota,
notas.media,notas.documentId,notas.photoId,notas.caption,notas.nombreArchivo FROM notas,blogs 
where notas.idUsuario={0} AND blogs.idUsuario={0} AND blogs.blog='{1}' AND notas.idBlog=blogs.idBlog """

INSERT_USUARIO='INSERT INTO usuarios(idUsuario,nombre,fechaIngreso) VALUES ({0},"{1}","{2}");'
INSERT_BLOG='INSERT INTO blogs(idBlog,blog,fechaCreacion,idUsuario) VALUES ("{0}","{1}","{2}",{3});'
INSERT_NOTA='INSERT INTO notas(idNota,fechaCreacion,nota,media,documentId,photoId,caption,nombreArchivo,idUsuario,idBlog) VALUES ("{0}","{1}","{2}","{3}","{4}","{5}","{6}","{7}",{8},"{9}");'

UPDATE_MEDIA_NOTA='UPDATE notas SET media= "{0}" WHERE idNota= "{1}";'

DELETE_NOTA='DELETE FROM notas where idNota={0};'
DELETE_BLOG='DELETE FROM blogs where idBlog={0};'
