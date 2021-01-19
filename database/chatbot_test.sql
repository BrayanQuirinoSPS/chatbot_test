--DROP DATABASE IF EXISTS chatbot_test;
--CREATE DATABASE chatbot_test;

--\c chatbot_test;

CREATE TABLE usuarios (
  idUsuario TEXT PRIMARY KEY NOT NULL,
  nombre TEXT,
  fechaIngreso TEXT
);

CREATE TABLE notas (
  idNota TEXT PRIMARY KEY NOT NULL,
  fechaCracion TEXT,
  nota TEXT,
  archivos BLOB,
  audios BLOB,
  fotos BLOB,
  idUsuario TEXT NOT NULL,
  idBlog TEXT,
  FOREIGN KEY (idUsuario) REFERENCES usuarios (idUsuario),
  FOREIGN KEY (idBlog) REFERENCES blogs (idBlog)
);

CREATE TABLE blogs (
  idBlog TEXT PRIMARY KEY NOT NULL,
  blog TEXT,
  fechaCreacion TEXT,
  idUsuario TEXT,
  FOREIGN KEY (idUsuario) REFERENCES usuarios (idUsuario)
);


INSERT INTO usuarios (idUsuario, nombre, fechaIngreso)
  VALUES ('aaa-bbb-ccc','Brayan Quirino','2021-01-19');