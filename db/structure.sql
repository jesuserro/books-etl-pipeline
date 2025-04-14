-- ==================================================
-- 1. Crear la base de datos y seleccionarla
-- ==================================================
CREATE DATABASE IF NOT EXISTS goodreads;

-- ==================================================
-- 2. Eliminar tablas si ya existen (opcional)
--    Esto evita errores si el script se ejecuta varias veces
-- ==================================================
SET FOREIGN_KEY_CHECKS = 0;

DROP TABLE IF EXISTS authors;


SET FOREIGN_KEY_CHECKS = 1;

-- ==================================================
-- 4. Tablas de Autores y Usuarios
-- ==================================================

-- Tabla para almacenar información de los autores
CREATE TABLE authors (
    author_id INT PRIMARY KEY,
    name VARCHAR(255),
    sex ENUM('M', 'F') DEFAULT NULL,
    born DATE,
    died DATE,
    age DECIMAL(10, 4),
    original_hometown VARCHAR(255),
    country VARCHAR(100),
    latitude DECIMAL(10, 8),
    longitude DECIMAL(11, 8),
    image_url VARCHAR(255),
    website VARCHAR(255),
    twitter VARCHAR(50),
    workcount INT,
    influence TEXT,
    genre VARCHAR(255),
    average_rate DECIMAL(3, 2),
    rating_count INT,
    review_count INT,
    fan_count INT,
    about TEXT
);