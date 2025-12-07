# Se empieza a realizar el llamado a cada modulo.
from api.api import ClienteAPI
from datos.gestor_datos import GestorDatos
from eda.procesador_eda import ProcesadorEDA

#----------------------------------------------------------------------------------------------------------------------#
# Clase = ClienteAPI
cliente_api = ClienteAPI()
cliente_api.coordenadas_paises()
cliente_api.clima_anual(2013, lat=10, lon=-84)
cliente_api.clima_rango_anios(2013, 2024, lat=10, lon=-84)
