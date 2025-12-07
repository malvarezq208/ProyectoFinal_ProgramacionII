# Importamos las librerías necesarias.
import pandas as pd # Maneja datos (DataFrames).
import numpy as np #Cálculos lógicos y matemáticos sobre cuadros y matrices
import os  # Manejar rutas de archivos.

#----------------------------------------------------------------------------------------------------------------------#
# Iniciamos la clase.
class ProcesadorEDA:  # Creamos la clase ProcesadorEDA la cual nos ayudara a realizar un analisis EDA.
    def __init__(self, DF_Turismo=pd.DataFrame()):  # Realizamos el constructor.
        self.__DF_Turismo = DF_Turismo  # Aqui tenemos nuestro atributo privado que almacena el DataFrame.
        self.__num_filas = DF_Turismo.shape[0]  # Aqui tenemos nuestros atributos privados que almacenan el numero de filas y columnas.
        self.__num_columnas = DF_Turismo.shape[1]

    # Creamos los propertys (getters) para acceder a los atributos privados.
    @property
    def DF_Turismo(self):
        return self.__DF_Turismo

    @property
    def num_filas(self):
        return self.__num_filas

    @property
    def num_columnas(self):
        return self.__num_columnas

    # Creamos los setters para que podamos modificar los atributos privados si es necesario.
    @DF_Turismo.setter
    def DF_Turismo(self, DF_Turismo):
        self.__DF_Turismo = DF_Turismo

    @num_filas.setter
    def num_filas(self, num_filas):
        self.__num_filas = num_filas

    @num_columnas.setter
    def num_columnas(self, num_columnas):
        self.__num_columnas = num_columnas

#-------------------------------------------------------------------------------------------------------------------#
# Iniciamos con la agregacion de metodos que necesitaremos para el analisis EDA.
# 1. Metodo en el cual obtendremos informacion general del Dataset que se nos a proporcionado.
    def informacion_turismo_cr(self):
        print("Informacion general del dataset")
        print(f"Primeros 5 registros del data set: \n{self.__DF_Turismo.head()}")
        print(f"Informacion general del dataset: \n{self.__DF_Turismo.info()}")
        print(f"Estadistica basica del dataset{self.__DF_Turismo.describe()}")

#-------------------------------------------------------------------------------------------------------------------#
# 2. Metodo con el que podremos limpiar textos ya sea el nombre de los paises.
    def limpiar_texto(self):
        columnas_texto = self.__DF_Turismo.select_dtypes(
            include=['object', 'category']).columns  # Selecciona las columnas de tipo texto.

        for columna in columnas_texto:
            self.__DF_Turismo[columna] = (self.__DF_Turismo[columna].astype(str).apply(
                lambda x: x.encode('utf-8', 'ignore').decode('utf-8', 'ignore')))  # Asegura que los datos sean de tipo string.

        print('El texto se ha limpiado correctamente')
#-------------------------------------------------------------------------------------------------------------------#
# 3. Metodo en el cual obtendremos aquellos datos nulos.
    def datos_nulos(self):
        total_nulos = self.__DF_Turismo.isnull().sum().sum() # Suma total de datos nulos en el DataFrame

        if total_nulos == 0: # Si no hay datos nulos
            print('No se encontraron datos nulos en el dataset')
        else: # Si hay datos nulos
            print('El dataset contiene datos nulos por columna:')
            print(self.__DF_Turismo.isnull().sum()) # Imprime la cantidad de datos nulos por columna

    # Dentro de este segundo metodo tendremos 2 metodos que ayuden a eliminar o imputar los datos nulos.
    # Eliminar los datos nulos.
    #def eliminar_datos_nulos(self):
        #self.__DF_Turismo.dropna(inplace=True)
        #print('Los datos nulos han sido eliminados')

    # Imputar los datos nulos (utilizar la media para los numericos y la moda para las categoricas). # Mejor opcion para que se pueda realizar el Modelo ML.
    def imputar_datos_nulos(self):
        total_nulos = self.__DF_Turismo.isnull().sum().sum() # Total de datos nulos en el DataFrame.

        if total_nulos == 0: # Si no hay datos nulos.
            print('No es necesario imputar: no existen datos nulos')
            return

        for columna in self.__DF_Turismo.columns: # Iterar sobre cada columna del DataFrame.
            if self.__DF_Turismo[columna].dtype in [np.float64, np.int64]: # Si la columna es numérica.
                self.__DF_Turismo[columna].fillna( # Imputar con la media.
                    self.__DF_Turismo[columna].mean(),
                    inplace=True
                )
            else: # Si la columna es categórica.
                self.__DF_Turismo[columna].fillna( # Imputar con la moda.
                    self.__DF_Turismo[columna].mode()[0],
                    inplace=True
                )
        print('Los datos nulos han sido imputados correctamente')

#-------------------------------------------------------------------------------------------------------------------#
# 4. Metodo en cual podremos obtener los valores duplicados.
    def datos_duplicados(self):
        print('Este dataset tiene los siguientes datos duplicados: \n')
        print(self.__DF_Turismo.duplicated().sum())

    # Ese metodo nos da el numero de filas duplicadas, en este nuevo metodo vamos a eliminar esos datos duplicados.
    def eliminar_datos_duplicados(self):
        self.__DF_Turismo.drop_duplicates(inplace=True)
        print('Los datos duplicados del dataset han sido eliminados correctamente')

#-------------------------------------------------------------------------------------------------------------------#
# 5. Metodo con el que vamos a corregir la columna 'Column1' por 'Años'.
    def colum_anios(self): # CSV turismo_anios.csv
        self.__DF_Turismo.rename(columns={'Column1': 'Años'}, inplace=True)
        print("La columna 'Column1' ha sido renombrada a 'Años' correctamente")

#----------------------------------------------------------------------------------------------------------------------#
 # 8. Metodo para poder guardar nuestros csvs limpios y guardarlos en la carpeta processed.
    def csv_limpio_turismo(self, ruta_guardar_csv='data/processed/turismo_anios_clean.csv'):
        carpeta = os.path.dirname(ruta_guardar_csv)  # Obtenemos la carpeta del path proporcionado.
        os.makedirs(carpeta, exist_ok=True)  # Creamos la carpeta si no existe.
        self.__DF_Turismo.to_csv(ruta_guardar_csv, index=False)  # Guardamos el DataFrame como un archivo CSV.
        print('El Dataset limpio se a guardado en la ruta:', {ruta_guardar_csv})

    def csv_limpio_zonas(self, ruta_guardar_csv='data/processed/zonas_aereas_clean.csv'):
        carpeta = os.path.dirname(ruta_guardar_csv)  # Obtenemos la carpeta del path proporcionado.
        os.makedirs(carpeta, exist_ok=True)  # Creamos la carpeta si no existe.
        self.__DF_Turismo.to_csv(ruta_guardar_csv, index=False)  # Guardamos el DataFrame como un archivo CSV.
        print('El Dataset limpio se a guardado en la ruta:', {ruta_guardar_csv})

#----------------------------------------------------------------------------------------------------------------------#
# 9. Metodo para realizar la limpieza general de los datasets.
    def ejecutar_eda_turismo(self):
        print("🔍 Iniciando ProcesadorEDA...\n")

        self.informacion_turismo_cr()
        self.limpiar_texto()
        self.datos_nulos()
        self.imputar_datos_nulos()
        self.datos_duplicados()
        self.eliminar_datos_duplicados()
        self.colum_anios()
        self.csv_limpio_turismo()

        print('Proceso EDA finalizado correctamente ✅ ')

    def ejecutar_eda_zonas(self):
        print("🔍 Iniciando ProcesadorEDA...\n")

        self.informacion_turismo_cr()
        self.limpiar_texto()
        self.datos_nulos()
        self.imputar_datos_nulos()
        self.datos_duplicados()
        self.eliminar_datos_duplicados()
        self.csv_limpio_zonas()

        print('Proceso EDA finalizado correctamente ✅ ')
