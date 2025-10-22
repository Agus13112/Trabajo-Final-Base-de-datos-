from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',  
    'database': 'jugadores'
}

@app.route('/', methods=['GET'])
def index():
    # Captura de filtros
    filtro_jugador = request.args.get('jugador', '').strip()
    filtro_equipo = request.args.get('equipo', '').strip()
    filtro_nacionalidad = request.args.get('nacionalidad', '').strip()
    filtro_posicion = request.args.get('posicion', '').strip()
    filtro_competicion = request.args.get('competicion', '').strip()
    edad_min = request.args.get('edad_min', '').strip()
    edad_max = request.args.get('edad_max', '').strip()
    goles_min = request.args.get('goles_min', '').strip()
    goles_max = request.args.get('goles_max', '').strip()
    
    # Captura de ordenamiento
    orden_por = request.args.get('orden_por', 'id')  # columna por la que ordenar
    orden_dir = request.args.get('orden_dir', 'ASC')  # dirección ASC o DESC

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)

    # Query base más simple y robusta
    sql = """
    SELECT 
        j.id AS Rk,
        j.nombre AS Player,
        COALESCE(n.nombre, '-') AS Nation,
        COALESCE(GROUP_CONCAT(DISTINCT p.nombre ORDER BY p.nombre SEPARATOR ', '), '-') AS Pos,
        COALESCE(GROUP_CONCAT(DISTINCT e.nombre ORDER BY e.nombre SEPARATOR ', '), '-') AS Squad,
        COALESCE(GROUP_CONCAT(DISTINCT c.nombre ORDER BY c.nombre SEPARATOR ', '), '-') AS Comp,
        j.edad AS Age,
        COALESCE(MAX(s.goles), 0) AS Gls,
        COALESCE(MAX(s.asistencias), 0) AS Ast
    FROM jugadores j
    LEFT JOIN nacionalidad n ON j.id_nacionalidad = n.id
    LEFT JOIN jugadores_posicion jp ON j.id = jp.id_jugador
    LEFT JOIN posicion p ON jp.id_posicion = p.id
    LEFT JOIN equipo e ON jp.id_equipo = e.id
    LEFT JOIN competicion c ON e.id_competicion = c.id
    LEFT JOIN jugadores_estadisticas je ON j.id = je.id_jugador AND jp.id_equipo = je.id_equipo
    LEFT JOIN estadisticas s ON je.id_estadisticas = s.id
    WHERE 1=1
    """

    params = []

    # Aplicar filtros solo si tienen valor
    if filtro_jugador:
        sql += " AND j.nombre LIKE %s"
        params.append(f'%{filtro_jugador}%')
    
    if filtro_nacionalidad:
        sql += " AND n.nombre = %s"
        params.append(filtro_nacionalidad)
    
    if filtro_equipo:
        sql += " AND e.nombre = %s"
        params.append(filtro_equipo)
    
    if filtro_posicion:
        sql += " AND p.nombre = %s"
        params.append(filtro_posicion)
    
    if filtro_competicion:
        sql += " AND c.nombre = %s"
        params.append(filtro_competicion)
    
    if edad_min:
        sql += " AND j.edad >= %s"
        params.append(int(edad_min))
    
    if edad_max:
        sql += " AND j.edad <= %s"
        params.append(int(edad_max))

    # Agrupar por jugador
    sql += " GROUP BY j.id, j.nombre, n.nombre, j.edad"

    # Filtros de goles (después del GROUP BY)
    having_conditions = []
    if goles_min:
        having_conditions.append("MAX(s.goles) >= %s")
        params.append(int(goles_min))
    
    if goles_max:
        having_conditions.append("MAX(s.goles) <= %s")
        params.append(int(goles_max))
    
    if having_conditions:
        sql += " HAVING " + " AND ".join(having_conditions)

    # Mapeo de columnas para ordenamiento seguro
    columnas_validas = {
        'id': 'j.id',
        'jugador': 'j.nombre',
        'nacion': 'n.nombre',
        'edad': 'j.edad',
        'goles': 'Gls',
        'asistencias': 'Ast'
    }
    
    # Validar columna y dirección
    columna_orden = columnas_validas.get(orden_por, 'j.id')
    direccion = 'DESC' if orden_dir == 'DESC' else 'ASC'
    
    sql += f" ORDER BY {columna_orden} {direccion} LIMIT 200;"

    try:
        cursor.execute(sql, params)
        datos = cursor.fetchall()
        print(f"Registros encontrados: {len(datos)}")  # Debug
    except Exception as e:
        print(f"Error en query: {e}")
        datos = []

    # Obtener listas para dropdowns
    try:
        cursor.execute("SELECT DISTINCT nombre FROM equipo WHERE nombre IS NOT NULL AND nombre != '' ORDER BY nombre;")
        equipos = [row['nombre'] for row in cursor.fetchall()]

        cursor.execute("SELECT DISTINCT nombre FROM nacionalidad WHERE nombre IS NOT NULL AND nombre != '' ORDER BY nombre;")
        nacionalidades = [row['nombre'] for row in cursor.fetchall()]

        cursor.execute("SELECT DISTINCT nombre FROM posicion WHERE nombre IS NOT NULL AND nombre != '' ORDER BY nombre;")
        posiciones = [row['nombre'] for row in cursor.fetchall()]

        cursor.execute("SELECT DISTINCT nombre FROM competicion WHERE nombre IS NOT NULL AND nombre != '' ORDER BY nombre;")
        competiciones = [row['nombre'] for row in cursor.fetchall()]
    except Exception as e:
        print(f"Error obteniendo dropdowns: {e}")
        equipos = []
        nacionalidades = []
        posiciones = []
        competiciones = []

    cursor.close()
    conn.close()

    return render_template('index.html',
                           datos=datos,
                           filtro_jugador=filtro_jugador,
                           filtro_equipo=filtro_equipo,
                           filtro_nacionalidad=filtro_nacionalidad,
                           filtro_posicion=filtro_posicion,
                           filtro_competicion=filtro_competicion,
                           edad_min=edad_min,
                           edad_max=edad_max,
                           goles_min=goles_min,
                           goles_max=goles_max,
                           equipos=equipos,
                           nacionalidades=nacionalidades,
                           posiciones=posiciones,
                           competiciones=competiciones,
                           orden_por=orden_por,
                           orden_dir=orden_dir)

if __name__ == '__main__':
    app.run(debug=True)