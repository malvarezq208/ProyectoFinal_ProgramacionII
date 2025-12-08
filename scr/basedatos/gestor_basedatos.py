#Conecta con SQLite, MySQL, PostgreSQL o SQL Server y permite ejecutar consultas

import sqlite3  #Libreria que me permite crear una base datos portable


import sqlite3
import pandas as pd

class BD:
    def __init__(self, db_name="MigracionCr.db"):
        # Inicializa la conexión a la base de datos
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.crear_tabla()

    def crear_tabla(self):
    # Creacion tabla Pais
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS Pais(
            IdPais INTEGER PRIMARY KEY AUTOINCREMENT,
            NombrePais NVARCHAR(100) NOT NULL,
            Latitud DECIMAL(9,6),
            Longitud DECIMAL(9,6),
            Nombre_Continente NVARCHAR(100) NOT NULL
        )
        """)

    # Creacion tabla Clima
        self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS Clima(
                    Id_Clima INTEGER PRIMARY KEY AUTOINCREMENT,
                    temp_max REAL,
                    temp_min REAL,
                    rain_mm REAL,
                    temp_avg REAL,
                    year INTEGER,   -- ahora es entero, no DATE
                    IdPais INTEGER NOT NULL,
                    FOREIGN KEY (IdPais) REFERENCES Pais(IdPais)
        )
        """)
    #Metodo que determina a cual continente pertece al pais segun las coordenadas
    def determinar_continente(self, lat, lon):
        # Clasifica continente según latitud/longitud
        if lat < -60:
            return "Antártida"
        elif -60 <= lat <= 83 and -170 <= lon <= -30:
            return "América"
        elif 35 <= lat <= 70 and -25 <= lon <= 60:
            return "Europa"
        elif -35 <= lat <= 37 and -20 <= lon <= 50:
            return "África"
        elif 5 <= lat <= 80 and 60 <= lon <= 180:
            return "Asia"
        elif -50 <= lat <= 10 and 110 <= lon <= 180:
            return "Oceanía"
        else:
            return "Desconocido"

    #Metodo para llenar la tabla Pais
    def insertar_paises(self, df: pd.DataFrame):
        # Asegurar que latitud y longitud sean numéricas
        df['Latitud'] = pd.to_numeric(df['Latitud'], errors='coerce')
        df['Longitud'] = pd.to_numeric(df['Longitud'], errors='coerce')

        for _, row in df.iterrows():
            continente = self.determinar_continente(row['Latitud'], row['Longitud'])
            self.cursor.execute("""
                INSERT INTO Pais (NombrePais, Latitud, Longitud, Nombre_Continente)
                VALUES (?, ?, ?, ?)
            """, (row['Pais'], row['Latitud'], row['Longitud'], continente))
        self.conn.commit()

    #Metodo para llenar la tabla Clima
    def cargar_clima(self, df, id_pais: int):

        for row in df.itertuples(index=False):
            self.cursor.execute("""
                INSERT INTO Clima (temp_max, temp_min, rain_mm, temp_avg, year, IdPais)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                row.temp_max,  # accede como atributo
                row.temp_min,
                row.rain_mm,
                row.temp_avg,
                row.year,
                id_pais
            ))
        self.conn.commit()


    #Metodo para poder realizar consultas a las tablas
    def consultar_tabla(self, nombre_tabla: str):

        query = f"SELECT * FROM {nombre_tabla}"
        df = pd.read_sql_query(query, self.conn)
        return df

    #Metodo para cerrar la conexion de la Base datos
    def cerrar(self):
        # Cierra la conexión
        self.conn.close()