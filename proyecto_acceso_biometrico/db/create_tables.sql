
DROP DATABASE IF EXISTS biopass_db;

CREATE DATABASE biopass_db;

\c biopass_db

CREATE TABLE IF NOT EXISTS usuarios (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    foto_blob BYTEA NOT NULL
);