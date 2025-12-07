# Se empieza a realizar el llamado a cada modulo.
from api.api import ClienteAPI
from datos.gestor_datos import GestorDatos
from eda.procesador_eda import ProcesadorEDA as eda

#----------------------------------------------------------------------------------------------------------------------#
# Clase = ClienteAPI / Instancia para consultar las API's
cliente_api = ClienteAPI()
cliente_api.coordenadas_paises()
cliente_api.clima_anual(2013, lat=10, lon=-84)
cliente_api.clima_rango_anios(2013, 2024, lat=10, lon=-84)

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