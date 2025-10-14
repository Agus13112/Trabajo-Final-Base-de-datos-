# Trabajo-Final-Base-de-datos-
Registro de jugadores de las 5 ligas de Europa

Hecho por Juan Manuel Comizzo y Agustin Vallejos

Paso 1:

Para realizar este trabajo final se tuvo que buscar una base de datos en formato csv. La cual la buscamos desde la pagina de Kaggle : https://www.kaggle.com/datasets.

El link de la base de base es el siguiente: 
https://www.kaggle.com/code/mahmoudredagamail/football-players-stats-2025-2026

Paso 2:

Despues de realizar la eleccion de la base de datos empezamos a hacer el Diagrama de Clase de acuerdo a los datos que elegimos.

Primero hicimos el diagrma de clases en formato papel(boceto), para tener un panorama de como armar el trabajo final. Consultando y preguntando por correciones y errores con Matias Nardelli y Ariel Nardelli. 

![WhatsApp Image 2025-10-10 at 13 34 56](https://github.com/user-attachments/assets/fc9e307f-cc21-481c-a5c2-9993cda0fe5e)

Una vez que el boceto del diagrama de clase quedo bien armado lo pasamos https://dbdiagram.io/d/68df19d7d2b621e4220d7ee7

![WhatsApp Image 2025-10-04 at 11 18 00](https://github.com/user-attachments/assets/b48f9210-7791-475e-8ee1-b30d0f7961d9)

Paso 3: 
  Creacion de la base de datos y sus tablas.

  CREATE TABLE `jugadores` (
  `id` integer PRIMARY KEY NOT NULL AUTO_INCREMENT,
  `nombre` varchar(255),
  `edad` integer,
  `nacimiento` date,
  `id_nacionalidad` integer,
  `jugador_posicion` integer,
  `jugador_estadisticas` integer
);

CREATE TABLE `nacionalidad` (
  `id` integer PRIMARY KEY NOT NULL AUTO_INCREMENT,
  `nombre` varchar(255)
);

CREATE TABLE `posicion` (
  `id` integer PRIMARY KEY NOT NULL AUTO_INCREMENT,
  `nombre` varchar(255)
);

CREATE TABLE `competicion` (
  `id` integer PRIMARY KEY NOT NULL AUTO_INCREMENT,
  `nombre` varchar(255)
);

CREATE TABLE `equipo` (
  `id` integer PRIMARY KEY NOT NULL AUTO_INCREMENT,
  `nombre` varchar(255),
  `id_competicion` integer
);

CREATE TABLE `estadisticas` (
  `id` integer PRIMARY KEY NOT NULL AUTO_INCREMENT,
  `goles` integer,
  `asistencias` integer,
  `tarjetas_amarillas` integer,
  `tarjetas_rojas` integer,
  `minutos_jugados` time
);

CREATE TABLE `jugadores_estadisticas` (
  `id_equipo` integer,
  `id_jugador` integer,
  `id_estadisticas` integer,
  PRIMARY KEY (`id_equipo`, `id_jugador`, `id_estadisticas`)
);

CREATE TABLE `jugadores_posicion` (
  `id_jugador` integer,
  `id_posicion` integer,
  `id_equipo` integer,
  PRIMARY KEY (`id_jugador`, `id_posicion`, `id_equipo`)
);

-- Cada jugador pertenece a una nacionalidad
ALTER TABLE `jugadores`
ADD CONSTRAINT `fk_jugador_nacionalidad`
FOREIGN KEY (`id_nacionalidad`) REFERENCES `nacionalidad` (`id`);

-- Cada equipo pertenece a una competición
ALTER TABLE `equipo`
ADD CONSTRAINT `fk_equipo_competicion`
FOREIGN KEY (`id_competicion`) REFERENCES `competicion` (`id`);

-- Relación muchos a muchos entre jugadores, estadísticas y equipos
ALTER TABLE `jugadores_estadisticas`
ADD FOREIGN KEY (`id_jugador`) REFERENCES `jugadores` (`id`);

ALTER TABLE `jugadores_estadisticas`
ADD FOREIGN KEY (`id_equipo`) REFERENCES `equipo` (`id`);

ALTER TABLE `jugadores_estadisticas`
ADD FOREIGN KEY (`id_estadisticas`) REFERENCES `estadisticas` (`id`);

-- Relación muchos a muchos entre jugadores, posición y equipos
ALTER TABLE `jugadores_posicion`
ADD FOREIGN KEY (`id_jugador`) REFERENCES `jugadores` (`id`);

ALTER TABLE `jugadores_posicion`
ADD FOREIGN KEY (`id_equipo`) REFERENCES `equipo` (`id`);

ALTER TABLE `jugadores_posicion`
ADD FOREIGN KEY (`id_posicion`) REFERENCES `posicion` (`id`);
  






Paso 4: 

cargamos el CSV en una tabla especifica para este mismo. Y empezamos la normalizacion de las tablas con los datos.


<img width="649" height="323" alt="imagen" src="https://github.com/user-attachments/assets/38697f59-5318-4063-910a-b485e11fc0f9" />

-----------------------------------------------------------------------------------------------------------------------------------

<img width="609" height="290" alt="imagen" src="https://github.com/user-attachments/assets/e8964e95-a927-4060-9d97-22e198b6539e" />

-----------------------------------------------------------------------------------------------------------------------------------

<img width="657" height="310" alt="imagen" src="https://github.com/user-attachments/assets/a229eff9-c117-4315-80fc-d334fdfd1f75" />

-----------------------------------------------------------------------------------------------------------------------------------

<img width="600" height="419" alt="imagen" src="https://github.com/user-attachments/assets/ee2fc081-b48b-4a7d-8c50-26d7c18f4c29" />

-----------------------------------------------------------------------------------------------------------------------------------

<img width="681" height="344" alt="imagen" src="https://github.com/user-attachments/assets/6c6bc3d7-924a-4665-948e-df57569a0190" />

-----------------------------------------------------------------------------------------------------------------------------------

<img width="571" height="383" alt="imagen" src="https://github.com/user-attachments/assets/b03c05e7-7f91-4502-9338-58cc82ad1dc8" />

-----------------------------------------------------------------------------------------------------------------------------------

<img width="564" height="457" alt="imagen" src="https://github.com/user-attachments/assets/20fa52c6-ab5a-4918-b1ca-730b7ad44d8b" />

-----------------------------------------------------------------------------------------------------------------------------------

<img width="606" height="420" alt="imagen" src="https://github.com/user-attachments/assets/e60dbf11-0872-4c6b-a617-d5e06f7ae52e" />








ACLARACION: No se utilizaron todos los datos que brindaba el csv sino que decidimos elegir los datos que nosotros consideramos mas importantes para abarcar el trabajo final.
