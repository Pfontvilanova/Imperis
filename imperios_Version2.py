import sqlite3
from datetime import datetime, timedelta

# Crear conexión con la base de datos SQLite
def crear_base_de_datos():
    conexion = sqlite3.connect("civilizaciones.db")
    cursor = conexion.cursor()

    # Tabla para civilizaciones (ya existente)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Civilizaciones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            inicio TEXT NOT NULL,
            fin TEXT NOT NULL
        )
    ''')

    # Tabla para periodos (ya existente)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Periodos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            civilizacion_id INTEGER NOT NULL,
            nombre_periodo TEXT NOT NULL,
            inicio_periodo TEXT NOT NULL,
            fin_periodo TEXT NOT NULL,
            FOREIGN KEY(civilizacion_id) REFERENCES Civilizaciones(id)
        )
    ''')

    # Tabla para fases (ya existente)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Fases (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            periodo_id INTEGER NOT NULL,
            nombre_fase TEXT NOT NULL,
            duracion INTEGER NOT NULL,
            inicio_fase TEXT NOT NULL,
            fin_fase TEXT NOT NULL,
            FOREIGN KEY(periodo_id) REFERENCES Periodos(id)
        )
    ''')

    # Nueva tabla para imperios
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Imperios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fase_id INTEGER NOT NULL,
            nombre TEXT NOT NULL,
            inicio TEXT NOT NULL,
            fin TEXT,
            duracion INTEGER DEFAULT 550,
            fechas_clave TEXT,
            FOREIGN KEY(fase_id) REFERENCES Fases(id)
        )
    ''')
    conexion.commit()
    conexion.close()

# Insertar un imperio
def insertar_imperio(fase_id, nombre, fecha_inicio, fecha_fin=None, fechas_clave=None):
    fecha_inicio = datetime.strptime(fecha_inicio, "%d/%m/%Y")
    fecha_fin = datetime.strptime(fecha_fin, "%d/%m/%Y") if fecha_fin else fecha_inicio + timedelta(days=550 * 365)  # 550 años por defecto
    conexion = sqlite3.connect("civilizaciones.db")
    cursor = conexion.cursor()
    cursor.execute('''
        INSERT INTO Imperios (fase_id, nombre, inicio, fin, duracion, fechas_clave)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (
        fase_id,
        nombre,
        fecha_inicio.strftime("%d/%m/%Y"),
        fecha_fin.strftime("%d/%m/%Y"),
        (fecha_fin - fecha_inicio).days // 365,  # Cálculo de la duración exacta en años
        fechas_clave
    ))
    conexion.commit()
    conexion.close()

# Ejemplo de uso inicial
if __name__ == "__main__":
    crear_base_de_datos()

    # Insertar un imperio de ejemplo dentro de una fase de unificación
    # Nota: Se requiere que fase_id sea un ID válido generado por las inserciones previas.
    insertar_imperio(
        fase_id=1,  # Cambiar según el ID real de la fase
        nombre="Imperio Ejemplo",
        fecha_inicio="01/01/1500",
        fecha_fin="01/01/2050",
        fechas_clave="{'fundacion': '01/01/1500', 'expansion': '01/01/1600'}"
    )