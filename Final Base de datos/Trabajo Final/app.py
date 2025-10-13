from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)

# 🔧 Configuración de la base de datos (ajustá estos datos según tu XAMPP/Heidi)
db_config = {
    'host': 'localhost',
    'user': 'root',          # tu usuario de MySQL
    'password': '',          # tu contraseña (vacía por defecto en XAMPP)
    'database': 'jugadores'
}

@app.route('/', methods=['GET'])
def index():
    filtro = request.args.get('filtro', '')

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)

    if filtro:
        sql = """
        SELECT Rk, Player, Nation, Pos, Squad, Comp, Age, Gls, Ast
        FROM `players_data_light-2025_2026`
        WHERE Player LIKE %s OR Squad LIKE %s
        LIMIT 100;
        """
        cursor.execute(sql, (f'%{filtro}%', f'%{filtro}%'))
    else:
        sql = """
        SELECT Rk, Player, Nation, Pos, Squad, Comp, Age, Gls, Ast
        FROM `players_data_light-2025_2026`
        LIMIT 100;
        """
        cursor.execute(sql)

    datos = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template('index.html', datos=datos, filtro=filtro)

if __name__ == '__main__':
    app.run(debug=True)
