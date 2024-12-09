DROP TABLE IF EXISTS tPermiso;
DROP TABLE IF EXISTS tUsuario ;
DROP TABLE IF EXISTS tPiezas ;
DROP TABLE IF EXISTS tTipoPieza;
DROP TABLE IF EXISTS tRol ;

-- Crear tabla tTipoPieza
CREATE TABLE tTipoPieza (
    ID_TIPO VARCHAR(4) PRIMARY KEY,
    NOMBRE VARCHAR(80) NOT NULL
);

-- Crear tabla tPiezas con eliminación en cascada
CREATE TABLE tPiezas (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    NOMBRE VARCHAR(255) NOT NULL,
    FABRICANTE VARCHAR(255) NOT NULL,
    ID_TIPO VARCHAR(4) NOT NULL,
    FOREIGN KEY (ID_TIPO) REFERENCES tTipoPieza(ID_TIPO) ON DELETE CASCADE
);

-- Crear tabla tRol
CREATE TABLE tRol (
    rolName VARCHAR(255) PRIMARY KEY,
    rolDes VARCHAR(255) NOT NULL,
    admin BOOLEAN NOT NULL
);

-- Crear tabla tPermiso con eliminación en cascada
CREATE TABLE tPermiso (
    rolName VARCHAR(255) NOT NULL,
    pantalla VARCHAR(255) NOT NULL,
    acceso BOOLEAN NOT NULL,
    modificacion BOOLEAN NOT NULL,
    PRIMARY KEY (rolName, pantalla),
    FOREIGN KEY (rolName) REFERENCES tRol(rolName) ON DELETE CASCADE
);

-- Crear tabla tUsuario con eliminación en cascada
CREATE TABLE tUsuario (
    nombre VARCHAR(255) PRIMARY KEY,
    password VARCHAR(255) NOT NULL,
    rolName VARCHAR(255) NOT NULL,
    FOREIGN KEY (rolName) REFERENCES tRol(rolName) ON DELETE CASCADE
);


-- Borrar los datos de las tablas
-- Desactiva las restricciones de claves foráneas temporalmente
--PRAGMA foreign_keys = OFF;

-- Borra los datos de todas las tablas
--DELETE FROM tPiezas;
--DELETE FROM tTipoPieza;
--DELETE FROM tUsuario;
--DELETE FROM tPermiso;
--DELETE FROM tRol;

--PRAGMA foreign_keys = ON;


-- Inserción de datos en tTipoPieza
INSERT INTO tTipoPieza (ID_TIPO, NOMBRE)
VALUES
    ('A', 'Chapa'),
    ('B', 'Motor'),
    ('C', 'Iluminacion'),
    ('D', 'Sensores'),
    ('E', 'Cristales');

-- Inserción de datos en tPiezas con marcas populares en España
INSERT INTO tPiezas (ID, NOMBRE, FABRICANTE, ID_TIPO)
VALUES
    (1, 'Faros delanteros', 'SEAT', 'C'),
    (2, 'Parachoques trasero', 'Renault', 'A'),
    (3, 'Motor TSI', 'Volkswagen', 'B'),
    (4, 'Sensor de aparcamiento', 'Citroen', 'D'),
    (5, 'Luna delantera', 'Peugeot', 'E'),
    (6, 'Bombillas luz de freno', 'Ford', 'C'),
    (7, 'Motor diesel HDi', 'Peugeot', 'B'),
    (8, 'Parachoques delantero', 'SEAT', 'A'),
    (9, 'Cristales laterales', 'Ford', 'E');

-- Inserción de datos en tRol
INSERT INTO tRol (rolName, rolDes, admin)
VALUES
    ('Administrador', 'Acceso total al sistema', 1),
    ('Usuario', 'Acceso limitado a ciertas funciones', 0),
    ('Invitado', 'Acceso muy restringido', 0);

-- Inserción de datos en tPermiso (permisos uniformes para cada rol)
INSERT INTO tPermiso (rolName, pantalla, acceso, modificacion)
VALUES
    -- Permisos para Administrador
    ('Administrador', 'Gestion de piezas', 1, 1),
    ('Administrador', 'Gestion de usuarios', 1, 1),
    ('Administrador', 'Ventas', 1, 1),

    -- Permisos para Usuario
    ('Usuario', 'Gestion de piezas', 1, 0),
    ('Usuario', 'Ventas', 1, 1),

    -- Permisos para Invitado
    ('Invitado', 'Gestion de piezas', 0, 0),
    ('Invitado', 'Ventas', 0, 0);

-- Inserción de datos en tUsuario (contraseñas iguales al nombre de usuario)
INSERT INTO tUsuario (nombre, password, rolName)
VALUES
    ('admin', 'admin', 'Administrador'),
    ('usuario1', 'usuario1', 'Usuario'),
    ('usuario2', 'usuario2', 'Usuario'),
    ('invitado', 'invitado', 'Invitado');
