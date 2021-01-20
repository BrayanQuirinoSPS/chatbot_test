--DROP DATABASE IF EXISTS chatbot_test;
--CREATE DATABASE chatbot_test;

--\c chatbot_test;
DROP TABLE IF EXISTS usuarios;
DROP TABLE IF EXISTS notas;
DROP TABLE IF EXISTS blogs;
CREATE TABLE usuarios (
  idUsuario NUMERIC PRIMARY KEY NOT NULL,
  nombre TEXT,
  fechaIngreso DATE
);

CREATE TABLE notas (
  idNota TEXT PRIMARY KEY NOT NULL,
  fechaCreacion DATE,
  nota TEXT,
  media BLOB,
  documentId TEXT,
  photoId TEXT,
  caption TEXT,
  nombreArchivo TEXT,
  idUsuario NUMERIC NOT NULL,
  idBlog TEXT,
  FOREIGN KEY (idUsuario) REFERENCES usuarios (idUsuario),
  FOREIGN KEY (idBlog) REFERENCES blogs (idBlog)
);

CREATE TABLE blogs (
  idBlog TEXT PRIMARY KEY NOT NULL,
  blog TEXT,
  fechaCreacion DATE,
  idUsuario NUMERIC,
  FOREIGN KEY (idUsuario) REFERENCES usuarios (idUsuario)
);


--INSERT INTO usuarios (idUsuario, nombre, fechaIngreso) VALUES (1,'Brayan Quirino','2021-01-19');
