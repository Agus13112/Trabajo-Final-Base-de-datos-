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

```sql
USE jugadores;

-- =============================================
-- PASO 1: Poblar COMPETICION
-- =============================================
INSERT INTO competicion (nombre)
SELECT DISTINCT Comp
FROM players_data_light-2025_2026
WHERE Comp IS NOT NULL
  AND TRIM(Comp) != '';

SELECT CONCAT('✓ Competiciones insertadas: ', COUNT(*), ' registros') AS resultado
FROM competicion;
```

-----------------------------------------------------------------------------------------------------------------------------------

```sql
-- =============================================
-- PASO 2: Poblar EQUIPO
-- =============================================
INSERT INTO equipo (nombre, id_competicion)
SELECT DISTINCT p.Squad, c.id
FROM players_data_light-2025_2026 p
INNER JOIN competicion c ON c.nombre = p.Comp
WHERE p.Squad IS NOT NULL
  AND TRIM(p.Squad) != '';

SELECT CONCAT('✓ Equipos insertados: ', COUNT(*), ' registros') AS resultado
FROM equipo;
```

-----------------------------------------------------------------------------------------------------------------------------------

```sql
-- =============================================
-- PASO 3: Poblar NACIONALIDAD
-- =============================================
-- Extrae el código de país (ej: "us USA" -> "USA")
INSERT INTO nacionalidad (nombre)
SELECT DISTINCT TRIM(SUBSTRING_INDEX(Nation, ' ', -1)) AS pais
FROM players_data_light-2025_2026
WHERE Nation IS NOT NULL
  AND TRIM(Nation) != ''
ORDER BY pais;

SELECT CONCAT('✓ Nacionalidades insertadas: ', COUNT(*), ' registros') AS resultado
FROM nacionalidad;
```

-----------------------------------------------------------------------------------------------------------------------------------

```sql
-- =============================================
-- PASO 4: Poblar POSICION
-- =============================================
-- Maneja posiciones múltiples separadas por coma (ej: "FW,MF")
INSERT INTO posicion (nombre)
SELECT DISTINCT pos_limpia
FROM (
    SELECT DISTINCT TRIM(SUBSTRING_INDEX(SUBSTRING_INDEX(p.Pos, ',', n.n), ',', -1)) AS pos_limpia
    FROM players_data_light-2025_2026 p
    CROSS JOIN (
        SELECT 1 AS n UNION ALL SELECT 2 UNION ALL SELECT 3 UNION ALL SELECT 4
    ) n
    WHERE p.Pos IS NOT NULL
      AND TRIM(p.Pos) != ''
      AND CHAR_LENGTH(p.Pos) - CHAR_LENGTH(REPLACE(p.Pos, ',', '')) >= n.n - 1
) posiciones
WHERE pos_limpia IS NOT NULL
  AND pos_limpia != ''
ORDER BY pos_limpia;

SELECT CONCAT('✓ Posiciones insertadas: ', COUNT(*), ' registros') AS resultado
FROM posicion;
```

-----------------------------------------------------------------------------------------------------------------------------------

```sql
-- =============================================
-- PASO 5: Poblar ESTADISTICAS
-- =============================================
-- Crea un registro de estadísticas por cada jugador
INSERT INTO estadisticas (goles, asistencias, tarjetas_amarillas, tarjetas_rojas, minutos_jugados)
SELECT
    IFNULL(Gls, 0) AS goles,
    IFNULL(Ast, 0) AS asistencias,
    IFNULL(CrdY, 0) AS tarjetas_amarillas,
    IFNULL(CrdR, 0) AS tarjetas_rojas,
    SEC_TO_TIME(IFNULL(Min, 0) * 60) AS minutos_jugados
FROM players_data_light-2025_2026
WHERE Player IS NOT NULL;

SELECT CONCAT('✓ Estadísticas insertadas: ', COUNT(*), ' registros') AS resultado
FROM estadisticas;
```

-----------------------------------------------------------------------------------------------------------------------------------

```sql
-- =============================================
-- PASO 6: Poblar JUGADORES
-- =============================================
INSERT INTO jugadores (nombre, edad, nacimiento, id_nacionalidad)
SELECT
    p.Player,
    FLOOR(p.Age) AS edad,
    CASE
        WHEN p.Born IS NOT NULL AND p.Born > 1900 THEN DATE(CONCAT(p.Born, '-01-01'))
        ELSE NULL
    END AS nacimiento,
    n.id AS id_nacionalidad
FROM players_data_light-2025_2026 p
LEFT JOIN nacionalidad n ON n.nombre = TRIM(SUBSTRING_INDEX(p.Nation, ' ', -1))
WHERE p.Player IS NOT NULL;

SELECT CONCAT('✓ Jugadores insertados: ', COUNT(*), ' registros') AS resultado
FROM jugadores;
```

-----------------------------------------------------------------------------------------------------------------------------------

```sql
-- Tabla temporal para asociar IDs
CREATE TEMPORARY TABLE temp_mapping AS
SELECT
    j.id AS id_jugador,
    e.id AS id_equipo,
    @row_num := @row_num + 1 AS row_num
FROM jugadores j
INNER JOIN players_data_light-2025_2026 p ON j.nombre = p.Player
INNER JOIN equipo e ON e.nombre = p.Squad
CROSS JOIN (SELECT @row_num := 0) r
ORDER BY j.id;

-- Insertar relaciones
INSERT INTO jugadores_estadisticas (id_equipo, id_jugador, id_estadisticas)
SELECT tm.id_equipo, tm.id_jugador, tm.row_num AS id_estadisticas
FROM temp_mapping tm;

DROP TEMPORARY TABLE temp_mapping;

SELECT CONCAT('✓ Relaciones jugador-estadísticas: ', COUNT(*), ' registros') AS resultado
FROM jugadores_estadisticas;
```

-----------------------------------------------------------------------------------------------------------------------------------

```sql
-- =============================================
-- PASO 8: Relacionar JUGADORES con POSICIONES
-- =============================================
-- Maneja posiciones múltiples por jugador
INSERT INTO jugadores_posicion (id_jugador, id_posicion, id_equipo)
SELECT DISTINCT
    j.id AS id_jugador,
    pos.id AS id_posicion,
    e.id AS id_equipo
FROM players_data_light-2025_2026 p
INNER JOIN jugadores j ON j.nombre = p.Player
INNER JOIN equipo e ON e.nombre = p.Squad
CROSS JOIN (
    SELECT 1 AS n UNION ALL SELECT 2 UNION ALL SELECT 3 UNION ALL SELECT 4
) nums
INNER JOIN posicion pos ON pos.nombre = TRIM(SUBSTRING_INDEX(SUBSTRING_INDEX(p.Pos, ',', nums.n), ',', -1))
WHERE p.Pos IS NOT NULL
  AND TRIM(p.Pos) != ''
  AND CHAR_LENGTH(p.Pos) - CHAR_LENGTH(REPLACE(p.Pos, ',', '')) >= nums.n - 1;

SELECT CONCAT('✓ Relaciones jugador-posiciones: ', COUNT(*), ' registros') AS resultado
FROM jugadores_posicion;
```







ACLARACION: No se utilizaron todos los datos que brindaba el csv sino que decidimos elegir los datos que nosotros consideramos mas importantes para abarcar el trabajo final.
