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
  






Paso 4: 

Creamos la base de datos en heidi, cargamos el CSV en una tabla especifica para este mismo. Y empezamos la normalizacion de las tablas con los datos.

-- ============================================
-- Script de Normalización de Datos
-- A: Tablas normalizadas (competicion, equipo, jugadores, etc.)
-- ============================================

USE jugadores;

-- ============================================
-- PASO 1: Poblar COMPETICION
-- ============================================
INSERT INTO competicion (nombre)
SELECT DISTINCT Comp
FROM `players_data_light-2025_2026`
WHERE Comp IS NOT NULL AND TRIM(Comp) != '';

SELECT CONCAT('✓ Competiciones insertadas: ', COUNT(*), ' registros') AS resultado FROM competicion;

-- ============================================
-- PASO 2: Poblar EQUIPO
-- ============================================
INSERT INTO equipo (nombre, id_competicion)
SELECT DISTINCT 
    p.Squad,
    c.id
FROM `players_data_light-2025_2026` p
INNER JOIN competicion c ON c.nombre = p.Comp
WHERE p.Squad IS NOT NULL AND TRIM(p.Squad) != '';

SELECT CONCAT('✓ Equipos insertados: ', COUNT(*), ' registros') AS resultado FROM equipo;

-- ============================================
-- PASO 3: Poblar NACIONALIDAD
-- ============================================
-- Extrae el código de país (ej: "us USA" -> "USA")
INSERT INTO nacionalidad (nombre)
SELECT DISTINCT 
    TRIM(SUBSTRING_INDEX(Nation, ' ', -1)) as pais
FROM `players_data_light-2025_2026`
WHERE Nation IS NOT NULL AND TRIM(Nation) != ''
ORDER BY pais;

SELECT CONCAT('✓ Nacionalidades insertadas: ', COUNT(*), ' registros') AS resultado FROM nacionalidad;

-- ============================================
-- PASO 4: Poblar POSICION
-- ============================================
-- Maneja posiciones múltiples separadas por coma (ej: "FW,MF")
INSERT INTO posicion (nombre)
SELECT DISTINCT pos_limpia
FROM (
    SELECT DISTINCT TRIM(SUBSTRING_INDEX(SUBSTRING_INDEX(p.Pos, ',', n.n), ',', -1)) as pos_limpia
    FROM `players_data_light-2025_2026` p
    CROSS JOIN (
        SELECT 1 as n UNION ALL SELECT 2 UNION ALL SELECT 3 UNION ALL SELECT 4
    ) n
    WHERE p.Pos IS NOT NULL 
    AND TRIM(p.Pos) != ''
    AND CHAR_LENGTH(p.Pos) - CHAR_LENGTH(REPLACE(p.Pos, ',', '')) >= n.n - 1
) posiciones
WHERE pos_limpia IS NOT NULL AND pos_limpia != ''
ORDER BY pos_limpia;

SELECT CONCAT('✓ Posiciones insertadas: ', COUNT(*), ' registros') AS resultado FROM posicion;

-- ============================================
-- PASO 5: Poblar ESTADISTICAS
-- ============================================
-- Crea un registro de estadísticas por cada jugador
INSERT INTO estadisticas (goles, asistencias, tarjetas_amarillas, tarjetas_rojas, minutos_jugados)
SELECT 
    IFNULL(Gls, 0) as goles,
    IFNULL(Ast, 0) as asistencias,
    IFNULL(CrdY, 0) as tarjetas_amarillas,
    IFNULL(CrdR, 0) as tarjetas_rojas,
    SEC_TO_TIME(IFNULL(Min, 0) * 60) as minutos_jugados
FROM `players_data_light-2025_2026`
WHERE Player IS NOT NULL;

SELECT CONCAT('✓ Estadísticas insertadas: ', COUNT(*), ' registros') AS resultado FROM estadisticas;

-- ============================================
-- PASO 6: Poblar JUGADORES
-- ============================================
INSERT INTO jugadores (nombre, edad, nacimiento, id_nacionalidad)
SELECT 
    p.Player,
    FLOOR(p.Age) as edad,
    CASE 
        WHEN p.Born IS NOT NULL AND p.Born > 1900 THEN DATE(CONCAT(p.Born, '-01-01'))
        ELSE NULL 
    END as nacimiento,
    n.id as id_nacionalidad
FROM `players_data_light-2025_2026` p
LEFT JOIN nacionalidad n ON n.nombre = TRIM(SUBSTRING_INDEX(p.Nation, ' ', -1))
WHERE p.Player IS NOT NULL;

SELECT CONCAT('✓ Jugadores insertados: ', COUNT(*), ' registros') AS resultado FROM jugadores;

-- ============================================
-- PASO 7: Relacionar JUGADORES con ESTADISTICAS y EQUIPOS
-- ============================================
-- Tabla temporal para mapear IDs
CREATE TEMPORARY TABLE temp_mapping AS
SELECT 
    j.id as id_jugador,
    e.id as id_equipo,
    @row_num := @row_num + 1 as row_num
FROM jugadores j
INNER JOIN `players_data_light-2025_2026` p ON j.nombre = p.Player
INNER JOIN equipo e ON e.nombre = p.Squad
CROSS JOIN (SELECT @row_num := 0) r
ORDER BY j.id;

-- Insertar relaciones
INSERT INTO jugadores_estadisticas (id_equipo, id_jugador, id_estadisticas)
SELECT 
    tm.id_equipo,
    tm.id_jugador,
    tm.row_num as id_estadisticas
FROM temp_mapping tm;

DROP TEMPORARY TABLE temp_mapping;

SELECT CONCAT('✓ Relaciones jugador-estadísticas: ', COUNT(*), ' registros') AS resultado 
FROM jugadores_estadisticas;

-- ============================================
-- PASO 8: Relacionar JUGADORES con POSICIONES
-- ============================================
-- Maneja posiciones múltiples por jugador
INSERT INTO jugadores_posicion (id_jugador, id_posicion, id_equipo)
SELECT DISTINCT
    j.id as id_jugador,
    pos.id as id_posicion,
    e.id as id_equipo
FROM `players_data_light-2025_2026` p
INNER JOIN jugadores j ON j.nombre = p.Player
INNER JOIN equipo e ON e.nombre = p.Squad
CROSS JOIN (
    SELECT 1 as n UNION ALL SELECT 2 UNION ALL SELECT 3 UNION ALL SELECT 4
) nums
INNER JOIN posicion pos ON pos.nombre = TRIM(SUBSTRING_INDEX(SUBSTRING_INDEX(p.Pos, ',', nums.n), ',', -1))
WHERE p.Pos IS NOT NULL 
AND TRIM(p.Pos) != ''
AND CHAR_LENGTH(p.Pos) - CHAR_LENGTH(REPLACE(p.Pos, ',', '')) >= nums.n - 1;

SELECT CONCAT('✓ Relaciones jugador-posiciones: ', COUNT(*), ' registros') AS resultado 
FROM jugadores_posicion;

-- Reactivar verificaciones
SET FOREIGN_KEY_CHECKS=1;
SET UNIQUE_CHECKS=1;

-- ============================================
-- RESUMEN FINAL
-- ============================================
SELECT '========================================' AS '';
SELECT 'RESUMEN DE NORMALIZACIÓN' AS '';
SELECT '========================================' AS '';
SELECT 'Competiciones' as Tabla, COUNT(*) as Total FROM competicion
UNION ALL
SELECT 'Equipos', COUNT(*) FROM equipo
UNION ALL
SELECT 'Nacionalidades', COUNT(*) FROM nacionalidad
UNION ALL
SELECT 'Posiciones', COUNT(*) FROM posicion
UNION ALL
SELECT 'Estadísticas', COUNT(*) FROM estadisticas
UNION ALL
SELECT 'Jugadores', COUNT(*) FROM jugadores
UNION ALL
SELECT 'Jugador-Estadísticas', COUNT(*) FROM jugadores_estadisticas
UNION ALL
SELECT 'Jugador-Posiciones', COUNT(*) FROM jugadores_posicion;

-- ============================================
-- EJEMPLOS DE CONSULTAS
-- ============================================
SELECT '========================================' AS '';
SELECT 'EJEMPLOS DE CONSULTAS' AS '';
SELECT '========================================' AS '';

-- Jugadores con sus equipos y competiciones
SELECT 
    j.nombre,
    j.edad,
    n.nombre as nacionalidad,
    e.nombre as equipo,
    c.nombre as competicion
FROM jugadores j
LEFT JOIN nacionalidad n ON j.id_nacionalidad = n.id
LEFT JOIN jugadores_estadisticas je ON j.id = je.id_jugador
LEFT JOIN equipo e ON je.id_equipo = e.id
LEFT JOIN competicion c ON e.id_competicion = c.id
LIMIT 5;








ACLARACION: No se utilizaron todos los datos que brindaba el csv sino que decidimos elegir los datos que nosotros consideramos mas importantes para abarcar el trabajo final.
