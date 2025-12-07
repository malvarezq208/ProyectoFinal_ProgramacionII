# En este .py se crea la clase para las API's.

# Importamos algunas librerias.
import pandas as pd  # Maneja datos (DataFrames).
import csv  # Lee y escribe los csv.
import requests  # Consulta a las API's.
import os  # Manejo de rutas de archivos.

base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")) #Obtiene la ruta raíz del proyecto sin importar desde dónde se ejecute el programa.

data_processed = os.path.join(base_dir, "data", "processed") #construye la ruta completa hacia la carpeta
#donde se guardarán los archivos CSV procesados (data/processed)

#----------------------------------------------------------------------------------------------------------------------#
class ClienteAPI():  # Creamos la clase.
    def __init__(self):  # Creamos el constructor
        pass  # Esta vacio porque no necesitamos inicializar nada porque utilizaremos metodos para llamar a las API's.

#----------------------------------------------------------------------------------------------------------------------#
# Metodo #1: Coordenadas de paises.
    def coordenadas_paises(self, filename='Coordenadas_Paises.csv'):  # Metodo para obtener las coordenadas de los paises y guardarlas en un csv.

        url = "https://restcountries.com/v3.1/all?fields=name,latlng" # URL de la API para obtener los datos de los paises
        response = requests.get(url) # Realizar la solicitud GET a la API
        countries = response.json() # Convertir la respuesta JSON en un diccionario de Python

        data = []  # Lista para construir el DataFrame

        for country in countries: # Iterar sobre cada pais en la respuesta
            name = country["name"]["common"] # Obtener el nombre comun del pais
            latlng = country.get("latlng", [None, None]) # Obtener las coordenadas latitud y longitud
            lat, lng = latlng # Asignar latitud y longitud

            data.append({# Agregar los datos a la lista
                "Pais": name,
                "Latitud": lat,
                "Longitud": lng
            })

        # Crear DataFrame
        df = pd.DataFrame(data)

        # Crear carpeta y ruta
        os.makedirs(data_processed, exist_ok=True) # Crear la carpeta si no existe
        ruta = os.path.join(data_processed, filename) # Definir la ruta del archivo

        # Guardar CSV
        df.to_csv(ruta, index=False, encoding="utf-8")

        print(f"Archivo {ruta} creado con éxito ✅") # Mensaje de éxito

        return df

#----------------------------------------------------------------------------------------------------------------------#
# Metodo #2: Clima Anual.
    def clima_anual(self, year, lat=10, lon=-84, filename=None):

        url = "https://archive-api.open-meteo.com/v1/archive"

        params = {
            "latitude": lat,
            "longitude": lon,
            "start_date": f"{year}-01-01",
            "end_date": f"{year}-12-31",
            "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum",
            "timezone": "auto"
        }

        response = requests.get(url, params=params)
        data = response.json()

        df = pd.DataFrame({
            "date": data["daily"]["time"],
            "temp_max": data["daily"]["temperature_2m_max"],
            "temp_min": data["daily"]["temperature_2m_min"],
            "rain_mm": data["daily"]["precipitation_sum"]
        })

        df["temp_avg"] = (df["temp_max"] + df["temp_min"]) / 2

        if filename is None:
            filename = f"clima_anual_{year}.csv"

        os.makedirs(data_processed, exist_ok=True)
        ruta = os.path.join(data_processed, filename)

        df.to_csv(ruta, index=False, encoding="utf-8")
        print(f"Archivo {ruta} creado con éxito ✅")

        return df

    #----------------------------------------------------------------------------------------------------------------------#
# Metodo #3: Clima por años (2013 - 2024)- (Se crea para que se pueda realizar la variable de entrada).
    def clima_rango_anios(self, inicio, fin, lat=10, lon=-84, filename='clima_resumen_anual.csv'):  # Metodo para obtener el clima anual de un lugar especifico (latitud y longitud) en un rango de años. 2013/2024

        url = "https://archive-api.open-meteo.com/v1/archive"  # URL de la API de clima historico.
        resumen = []  # Lista para almacenar el resumen anual.

        for year in range(inicio, fin + 1):  # Iteramos sobre el rango de años.
            # Parametros para la peticion a la API.
            params = {
                "latitude": lat,
                "longitude": lon,
                "start_date": f"{year}-01-01",
                "end_date": f"{year}-12-31",
                "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum",
                "timezone": "auto"
            }

            response = requests.get(url, params=params)  # Petición al API
            data = response.json()  # Convertimos la respuesta a formato JSON.

            tmax = data["daily"]["temperature_2m_max"]
            tmin = data["daily"]["temperature_2m_min"]
            rain = data["daily"]["precipitation_sum"]

            avg_max = sum(tmax) / len(tmax)
            avg_min = sum(tmin) / len(tmin)
            avg_rain = sum(rain) / len(rain)
            avg_temp = (avg_max + avg_min) / 2

            resumen.append({  # Agregamos el resumen anual a la lista.
                "year": year,
                "temp_max": round(avg_max, 2),
                "temp_min": round(avg_min, 2),
                "rain_mm": round(avg_rain, 2),
                "temp_avg": round(avg_temp, 2)
            })

        df = pd.DataFrame(resumen)  # Creamos el DataFrame con el resumen anual.

        os.makedirs(data_processed, exist_ok=True)
        ruta = os.path.join(data_processed, filename)

        df.to_csv(ruta, index=False, encoding="utf-8")  # Guardar CSV
        print(f"Archivo '{ruta}' creado con éxito ✅")  # Mensaje de que se creo el csv y lo envio a la ruta.

        return df
