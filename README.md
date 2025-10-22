# ⚽ Registro de Jugadores de las 5 Ligas de Europa

**Proyecto realizado por:**  
🧑‍💻 Juan Manuel Comizzo  
🧑‍💻 Agustín Vallejos  

---

## 📌 Paso 1: Selección de la Base de Datos

Para realizar este trabajo final, se buscó una base de datos en formato **CSV**, proveniente del sitio [Kaggle](https://www.kaggle.com/datasets).

📂 **Fuente de la base de datos:**  
[Football Players Stats 2025-2026](https://www.kaggle.com/code/mahmoudredagamail/football-players-stats-2025-2026)

---

## 🧩 Paso 2: Diagrama de Clases

Luego de elegir la base de datos, se realizó el **diagrama de clases** de acuerdo con los datos seleccionados.

El primer boceto fue hecho a mano, para tener una visión general de cómo estructurar el trabajo final.  
Durante el proceso se realizaron **consultas y correcciones** junto a **Matías Nardelli** y **Ariel Nardelli** para asegurar la correcta organización de las entidades y sus relaciones.

![WhatsApp Image 2025-10-10 at 13 34 56](https://github.com/user-attachments/assets/fc9e307f-cc21-481c-a5c2-9993cda0fe5e)

Una vez que el boceto del diagrama de clase quedo bien armado lo pasamos https://dbdiagram.io/d/68df19d7d2b621e4220d7ee7

![WhatsApp Image 2025-10-04 at 11 18 00](https://github.com/user-attachments/assets/b48f9210-7791-475e-8ee1-b30d0f7961d9)

## 🏗️ Paso 3: Creación de la Base de Datos y sus Tablas

En esta etapa se procedió a la **creación de la base de datos** y las **tablas correspondientes** utilizando **SQL**.  
El objetivo fue estructurar la información de manera **normalizada**, garantizando la integridad y consistencia de los datos.
  
```sql
CREATE TABLE `jugadores` (
  `id` INTEGER PRIMARY KEY NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(255),
  `edad` INTEGER,
  `nacimiento` DATE,
  `id_nacionalidad` INTEGER,
  `jugador_posicion` INTEGER,
  `jugador_estadisticas` INTEGER
);

```

-----------------------------------------------------------------------------------------------------------------------------------

```sql
CREATE TABLE `nacionalidad` (
  `id` INTEGER PRIMARY KEY NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(255)
);
```

-----------------------------------------------------------------------------------------------------------------------------------

```sql
CREATE TABLE `posicion` (
  `id` INTEGER PRIMARY KEY NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(255)
);
```

-----------------------------------------------------------------------------------------------------------------------------------

```sql
CREATE TABLE `competicion` (
  `id` INTEGER PRIMARY KEY NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(255)
);
```

-----------------------------------------------------------------------------------------------------------------------------------

```sql
CREATE TABLE `equipo` (
  `id` INTEGER PRIMARY KEY NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(255),
  `id_competicion` INTEGER
);
```

-----------------------------------------------------------------------------------------------------------------------------------

```sql
CREATE TABLE `estadisticas` (
  `id` INTEGER PRIMARY KEY NOT NULL AUTO_INCREMENT,
  `goles` INTEGER,
  `asistencias` INTEGER,
  `tarjetas_amarillas` INTEGER,
  `tarjetas_rojas` INTEGER,
  `minutos_jugados` TIME
);
```

-----------------------------------------------------------------------------------------------------------------------------------

```sql
CREATE TABLE `jugadores_estadisticas` (
  `id_equipo` INTEGER,
  `id_jugador` INTEGER,
  `id_estadisticas` INTEGER,
  PRIMARY KEY (`id_equipo`, `id_jugador`, `id_estadisticas`)
);
```

-----------------------------------------------------------------------------------------------------------------------------------

```sql
CREATE TABLE `jugadores_posicion` (
  `id_jugador` INTEGER,
  `id_posicion` INTEGER,
  `id_equipo` INTEGER,
  PRIMARY KEY (`id_jugador`, `id_posicion`, `id_equipo`)
);
```

-----------------------------------------------------------------------------------------------------------------------------------

```sql
-- Cada jugador pertenece a una nacionalidad
ALTER TABLE `jugadores`
ADD CONSTRAINT `fk_jugador_nacionalidad`
FOREIGN KEY (`id_nacionalidad`) REFERENCES `nacionalidad`(`id`);

-- Cada equipo pertenece a una competición
ALTER TABLE `equipo`
ADD CONSTRAINT `fk_equipo_competicion`
FOREIGN KEY (`id_competicion`) REFERENCES `competicion`(`id`);

-- Relación muchos a muchos entre jugadores, estadísticas y equipos
ALTER TABLE `jugadores_estadisticas`
ADD FOREIGN KEY (`id_jugador`) REFERENCES `jugadores`(`id`);

ALTER TABLE `jugadores_estadisticas`
ADD FOREIGN KEY (`id_equipo`) REFERENCES `equipo`(`id`);

ALTER TABLE `jugadores_estadisticas`
ADD FOREIGN KEY (`id_estadisticas`) REFERENCES `estadisticas`(`id`);

-- Relación muchos a muchos entre jugadores, posición y equipos
ALTER TABLE `jugadores_posicion`
ADD FOREIGN KEY (`id_jugador`) REFERENCES `jugadores`(`id`);

ALTER TABLE `jugadores_posicion`
ADD FOREIGN KEY (`id_equipo`) REFERENCES `equipo`(`id`);

ALTER TABLE `jugadores_posicion`
ADD FOREIGN KEY (`id_posicion`) REFERENCES `posicion`(`id`);
```


  
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
