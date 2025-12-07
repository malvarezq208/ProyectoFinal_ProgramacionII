# Importamos algunas librerias.
import pandas as pd # Manipulacion de datos
import numpy as np # Operaciones numericas
import os # Manejo de rutas y archivos
import unicodedata # Normalizacion de texto
import re # Expresiones regulares

base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")) # Directorio base del proyecto
data_processed = os.path.join(base_dir, "data", "processed") # Ruta para guardar los datos procesados

#----------------------------------------------------------------------------------------------------------------------#

class ProcesadorEDA: # Clase para realizar EDA en DataFrames de pandas.
    def __init__(self, df: pd.DataFrame): # Constructor de la clase.
        if df.empty: # Si el DataFrame esta vacio.
            raise ValueError('El DataFrame está vacío al iniciar ProcesadorEDA') # Validacion de DataFrame vacio.
        self.df = df.copy() # Copia del DataFrame para evitar modificar el original.

#----------------------------------------------------------------------------------------------------------------------#
# Metodo #1: Informacion general de los csv.
    def informacion(self):
        print('Información general del dataset')
        print(self.df.head()) # Muestra las primeras filas del DataFrame.
        print(self.df.info()) # Muestra informacion del DataFrame.

#----------------------------------------------------------------------------------------------------------------------#
# Metodo #2: Limpiamos el texto de los csv.
    def limpiar_texto(self):
        self.df.columns = ( # Limpiamos los nombres de las columnas
            self.df.columns
            .astype(str)
            .map(lambda x: unicodedata.normalize("NFKD", x))
            .map(lambda x: x.encode("ascii", "ignore").decode("utf-8"))
            .str.replace(r"[^A-Za-z0-9_ ]", "", regex=True)
            .str.strip()
            .str.upper()
        )

        columnas_texto = self.df.select_dtypes(include="object").columns # Seleccionamos las columnas de tipo texto

        for col in columnas_texto: # Limpiamos cada columna de texto
            self.df[col] = (
                self.df[col]
                .fillna("")
                .astype(str)
                .map(lambda x: unicodedata.normalize("NFKD", x))
                .map(lambda x: x.encode("ascii", "ignore").decode("utf-8"))
                .str.replace(r"[^A-Za-z0-9 ]", "", regex=True)
                .str.strip()
                .str.upper()
            )

        print('✅Textos limpios correctamente')

#----------------------------------------------------------------------------------------------------------------------#
# Metodo #3: Este metodo nos ayudara ha saber si existen datos nulos, y al tener que realizar un MODELO ML dejaremos que los NaN sean imputados.
    def datos_nulos(self):
        total = self.df.isnull().sum().sum() # Contamos el total de datos nulos
        if total == 0: # Si no hay datos nulos
            print('No existen datos nulos')
        else: # Si hay datos nulos
            print('Nulos por columna:')
            print(self.df.isnull().sum()) # Mostramos los datos nulos por columna


    def imputar_datos_nulos(self): # Imputacion de datos nulos
        if self.df.isnull().sum().sum() == 0: # Si no hay datos nulos
            print('No es necesario imputar')
            return

        for col in self.df.columns: # Imputamos los datos nulos
            if self.df[col].dtype in ["float64", "int64"]: # Si la columna es numerica
                self.df[col].fillna(self.df[col].mean(), inplace=True) # Imputamos con la media
            else: # Si la columna es de texto
                self.df[col].fillna(self.df[col].mode()[0], inplace=True) # Imputamos con la moda

        print('✅Datos nulos imputados correctamente')

#----------------------------------------------------------------------------------------------------------------------#
# Metodo #4: Nos ayuda a eliminar los datos duplicados.
    def eliminar_duplicados(self):
        dup = self.df.duplicated().sum() # Contamos los duplicados
        if dup == 0: # Si no hay duplicados
            print('No hay duplicados')
        else: # Si hay duplicados
            self.df.drop_duplicates(inplace=True)
            print(f"✅{dup} duplicados eliminados")

#----------------------------------------------------------------------------------------------------------------------#
# Metodo #5: Corrige la columa annios del csv turismo.
    def columna_anios(self):
        for col in self.df.columns: # Recorremos las columnas
            col_norm = (
                unicodedata.normalize("NFKD", col) # Normalizamos el nombre de la columna
                .encode("ascii", "ignore") # Eliminamos acentos
                .decode("utf-8") # Decodificamos a utf-8
                .strip() # Eliminamos espacios en blanco
                .upper() # Convertimos a mayusculas
            )

            if col_norm in ["COLUMN1", "ICOLUMN1", "ANNIOS", "ANIOS"]: # Posibles nombres de la columna AÑOS
                self.df.rename(columns={col: "ANNIOS"}, inplace=True) # Renombramos la columna a AÑOS
                print('✅Columna AÑOS corregida')
                return

#----------------------------------------------------------------------------------------------------------------------#
# Metodo #6: Guarada los csv.
    def guardar_csv(self, nombre): # Guarda el DataFrame en un archivo CSV
        os.makedirs(data_processed, exist_ok=True) # Creamos el directorio si no existe
        ruta = os.path.join(data_processed, nombre) # Ruta completa del archivo
        self.df.to_csv(ruta, index=False, encoding="utf-8") # Guardamos el DataFrame en un archivo CSV
        print(f"CSV guardado en: {ruta}")

#----------------------------------------------------------------------------------------------------------------------#
# Metodo #7: Ejecutar EDA (metodos)
    def ejecutar_eda(self, archivo_salida):
        print("🔍 Iniciando EDA...\n")
        self.informacion()
        self.columna_anios()
        self.limpiar_texto()
        self.datos_nulos()
        self.imputar_datos_nulos()
        self.eliminar_duplicados()
        self.guardar_csv(archivo_salida)
        print("✅ Proceso EDA finalizado")