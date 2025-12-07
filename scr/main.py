# Se empieza a realizar el llamado a cada modulo.
from api.api import ClienteAPI
from datos.gestor_datos import GestorDatos
from eda.procesador_eda import ProcesadorEDA as eda
from basedatos.gestor_basedatos import BD
import pandas as pd

#----------------------------------------------------------------------------------------------------------------------#
# Clase = ClienteAPI / Instancia para consultar las API's
#cliente_api = ClienteAPI()
#cliente_api.coordenadas_paises()
#cliente_api.clima_anual(2013, lat=10, lon=-84)
#cliente_api.clima_rango_anios(2013, 2024, lat=10, lon=-84)

#----------------------------------------------------------------------------------------------------------------------#
# Clase = GestorDatos / Instancia para cargar los datos
turismo = GestorDatos('data/raw/turismo_anios.csv')
# Se llama al metodo de la clase para leer el archivo
turismo.leer_archivo()

zonas = GestorDatos('data/raw/zonas_aerea.csv')
zonas.leer_archivo()

#----------------------------------------------------------------------------------------------------------------------#
# Clase = ProcesadorEDA / Instacia para poder limpiar el csv.
eda_turismo = eda(turismo.df)
eda_turismo.ejecutar_eda('turismo_anios_clean.csv')

eda_zonas = eda(zonas.df)
eda_zonas.ejecutar_eda('zonas_aereas_clean.csv')

#----------------------------------------------------------------------------------------------------------------------#
#Ejecucion base datos

#----------------------------------------------------------------------------------------------------------------------#
#Carga de los archivos CSV processed

#Archivo clima_anual_2013.csv
clima_anual=GestorDatos('data/processed/clima_anual_2013.csv')
df_clima_anual=pd.DataFrame(clima_anual.retornar_csv())


#Archivo clima_resumen_anual.csv
clima_resumen_anual=GestorDatos('data/processed/clima_resumen_anual.csv')
df_clima_resumen=pd.DataFrame(clima_resumen_anual.retornar_csv())


#Archivo Coordenadas_paises.csv
paises=GestorDatos('data/processed/Coordenadas_paises.csv')
df_paises=pd.DataFrame(paises.retornar_csv())


#Archivo turismo_anios_clean.csv
turismo_anual=GestorDatos('data/processed/turismo_anios_clean.csv')
df_turismo_anual=pd.DataFrame(turismo_anual.retornar_csv())


#Archivo zonas_aereas_clean.csv
zonas_aereas=GestorDatos('data/processed/zonas_aereas_clean.csv')
df_zonas_aereas=pd.DataFrame(zonas_aereas.retornar_csv())


#----------------------------------------------------------------------------------------------------------------------#
#Creacion base datos
basedatos=BD("MigracionCR")
basedatos.crear_tabla()

#----------------------------------------------------------------------------------------------------------------------#
#Insert de las tablas
#Tabla Paises
basedatos.insertar_paises(df_paises)

#Tabla Clima
basedatos.cargar_clima(df_clima_resumen,44)

#----------------------------------------------------------------------------------------------------------------------#
#Consulta de las tablas

#Consulta Tabla Pais
consulta_pais=basedatos.consultar_tabla('Pais')
print(f"Tabla Pais \n {consulta_pais}")

#Consulta Tabla Clima Anual Costa Rica
consulta_clima=basedatos.consultar_tabla('Clima')
print(f"Tabla Clima Anual CR \n {consulta_clima}")





