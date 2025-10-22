import mysql.connector
import pandas as pd

# === CONFIGURACIÓN DE CONEXIÓN A MySQL ===
try:
    conexion = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="jugadores"
    )
    cursor = conexion.cursor()
except mysql.connector.Error as err:
    print(f"Error de conexión: {err}")
    exit(1)

# === RUTA DEL CSV ===
ruta_csv = r"D:\3er año\Base de datos\Basaes de datos\a\players_data_light-2025_2026.csv"

# === LEER EL CSV ===
print("Leyendo archivo CSV...")
df = pd.read_csv(ruta_csv)
print(f"Archivo leído correctamente. Filas: {len(df)}, Columnas: {len(df.columns)}")

# === NOMBRE DE LA TABLA ===
tabla = "`players_data_light-2025_2026`"

# === CREAR TABLA SI NO EXISTE ===
create_table_sql = f"""
CREATE TABLE IF NOT EXISTS {tabla} (
    {', '.join([f'`{col}` VARCHAR(255)' for col in df.columns])}
)
"""
try:
    cursor.execute(create_table_sql)
    conexion.commit()
except Exception as e:
    print(f"⚠️ Error al crear la tabla: {e}")
    conexion.rollback()

# === NOMBRE DE LA TABLA ===
tabla = "`players_data_light-2025_2026`"

# === CONSTRUCCIÓN SEGURA DEL INSERT ===
columnas = df.columns.tolist()
column_names = ", ".join([f"`{col}`" for col in columnas])  # importante: usa comillas invertidas
placeholders = ", ".join(["%s"] * len(columnas))

sql = f"INSERT INTO {tabla} ({column_names}) VALUES ({placeholders})"

# === INSERTAR POR LOTES ===
print("Insertando registros en MySQL...")
batch_size = 500

for i in range(0, len(df), batch_size):
    batch = df.iloc[i:i+batch_size]
    try:
        cursor.executemany(sql, [tuple(x) for x in batch.to_numpy()])
        conexion.commit()
        print(f"Insertadas {i + len(batch)} filas...")
    except Exception as e:
        print(f"⚠️ Error en lote {i}: {e}")
        conexion.rollback()

print("✅ Importación completada con éxito.")
cursor.close()
conexion.close()
