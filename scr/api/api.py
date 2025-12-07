# En este .py se crea la clase para las API's.

# Importamos algunas librerias.
import pandas as pd  # Maneja datos (DataFrames).
import csv  # Lee y escribe los csv.
import requests  # Consulta a las API's.
import os  # Manejo de rutas de archivos.

#----------------------------------------------------------------------------------------------------------------------#
class ClienteAPI():  # Creamos la clase.
    def __init__(self):  # Creamos el constructor
        pass  # Esta vacio porque no necesitamos inicializar nada porque utilizaremos metodos para llamar a las API's.

#----------------------------------------------------------------------------------------------------------------------#
# Metodo #1: Coordenadas de paises.
    def coordenadas_paises(self,
                           filename='Coordenadas_Paises.csv'):  # Metodo para obtener las coordenadas de los paises y guardarlas en un csv.
        url = 'https://restcountries.com/v3.1/all?fields=name,latlng'  # URL de la API.
        response = requests.get(url)  # Hacemos la peticion a la API.
        countries = response.json()  # Convertimos la respuesta a formato JSON.

        carpeta = 'data/processed' # Aqui definimos donde va a ir guardado este csv
        os.makedirs(carpeta, exist_ok=True) # Si la carpeta no existe, la crea.

        ruta = os.path.join(carpeta, filename) # Se une la carpeta mas el nombre del csv.

        with open(filename, 'w', newline="", encoding='utf-8') as csvfile:  # Abrimos el archivo CSV para escribir.
            writer = csv.writer(csvfile)  # Creamos el objeto writer (se usa para escribir datos en archivos (como texto o CSV).
            writer.writerow(['Pais', 'Latitud', 'Longitud'])  # Escribimos el encabezzado del CSV.

            for country in countries:  # Iteramos sobre los paises obtenidos de la API.
                name = country['name']['common']  # Obtenemos el nombre comun del pais.
                latlng = country.get('latlng', [None, None])  # Obtenemos las coordenadas (latitud y longitud). Si no existen, asignamos [None, None].
                lat, lng = latlng
                writer.writerow([name, lat, lng])  # Escribimos una fila en el CSV con el nombre del pais, latitud y longitud.

        print(f"Archivo {ruta} creado con éxito ✅")  # Mensaje de que se creo el csv y lo envio a la ruta.

#----------------------------------------------------------------------------------------------------------------------#
# Metodo #2: Clima Anual.
    def clima_anual(self, year, lat=10, lon=-84, filename=None):  # Metodo para obtener el clima anual de un lugar especifico (latitud y longitud). CR
        url = "https://archive-api.open-meteo.com/v1/archive"  # URL de la API de clima historico.

        params = {  # Parametros para la peticion a la API.
            "latitude": lat,
            "longitude": lon,
            "start_date": f"{year}-01-01",
            "end_date": f"{year}-12-31",
            "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum",
            "timezone": "auto"
        }

        # Petición al API
        response = requests.get(url, params=params)  # Hacemos la peticion a la API con los parametros.
        data = response.json()  # Convertimos la respuesta a formato JSON.

        # Extraer datos diarios
        days = data["daily"]["time"]  # Fechas
        tmax = data["daily"]["temperature_2m_max"]  # Temperatura maxima
        tmin = data["daily"]["temperature_2m_min"]  # Temperatura minima
        rain = data["daily"]["precipitation_sum"]  # Precipitacion

        # DataFrame con los datos
        df = pd.DataFrame({
            "date": days,
            "temp_max": tmax,
            "temp_min": tmin,
            "rain_mm": rain
        })

        # Columna temperatura promedio
        df["temp_avg"] = (df["temp_max"] + df["temp_min"]) / 2

        # Nombre del CSV
        if filename is None:
            filename = f"clima_anual_{year}.csv"

        carpeta = 'data/processed'  # Aqui definimos donde va a ir guardado este csv
        os.makedirs(carpeta, exist_ok=True)  # Si la carpeta no existe, la crea.

        ruta = os.path.join(carpeta, filename)  # Se une la carpeta mas el nombre del csv.

        df.to_csv(ruta, index=False)  # Guardar CSV
        print(f"Archivo {ruta} creado con éxito ✅")  # Mensaje de que se creo el csv y lo envio a la ruta.

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

        carpeta = 'data/processed'  # Aqui definimos donde va a ir guardado este csv
        os.makedirs(carpeta, exist_ok=True)  # Si la carpeta no existe, la crea.

        ruta = os.path.join(carpeta, filename)  # Se une la carpeta mas el nombre del csv.

        df.to_csv(ruta, index=False, encoding="utf-8")  # Guardar CSV
        print(f"Archivo '{ruta}' creado con éxito ✅")  # Mensaje de que se creo el csv y lo envio a la ruta.

        return df
