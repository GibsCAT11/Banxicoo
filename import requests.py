#!/usr/bin/env python3
import os
import requests
import pandas as pd
from datetime import datetime
import logging
from dotenv import load_dotenv

# Configuración del registro de eventos
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Cargar variables de entorno desde el archivo banx.env
load_dotenv('banx.env')

def obtener_datos_banxico(token, serie, fecha_inicio, fecha_fin):
    url = f"https://www.banxico.org.mx/SieAPIRest/service/v1/series/{serie}/datos/{fecha_inicio}/{fecha_fin}"
    headers = {"Bmx-Token": token}
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Lanza excepción para códigos 4xx/5xx
        datos = response.json()
        
        # Verificar que la estructura de la respuesta sea la esperada
        if 'bmx' in datos and 'series' in datos['bmx'] and len(datos['bmx']['series']) > 0:
            serie_datos = datos['bmx']['series'][0].get('datos', [])
            return serie_datos
        else:
            logging.error("La respuesta no contiene los datos esperados.")
            return []
    except requests.exceptions.RequestException as e:
        logging.error(f"Error en la solicitud HTTP: {e}")
        return []
    except ValueError as e:
        logging.error(f"Error al procesar la respuesta JSON: {e}")
        return []

def main():
    # Obtener el token desde las variables de entorno
    token = os.getenv("BANXICO_TOKEN")
    if not token:
        logging.error("El token de Banxico no está configurado en las variables de entorno.")
        exit(1)

    # Configuración del servicio
    serie = "SF43718"        # Serie de ejemplo
    fecha_inicio = "2015-01-01"
    fecha_fin = datetime.now().strftime("%Y-%m-%d")  # Fecha actual

    # Obtener los datos de Banxico
    datos = obtener_datos_banxico(token, serie, fecha_inicio, fecha_fin)

    if datos:
        # Crear un DataFrame para mostrar los datos en tabla
        df = pd.DataFrame(datos)
        logging.info("Datos obtenidos exitosamente.")
        
        # Imprimir un resumen de los datos en consola (primeras y últimas 5 filas)
        print("Primeras 5 filas de datos:")
        print(df.head())
        print("\nÚltimas 5 filas de datos:")
        print(df.tail())
        
        # Guardar en archivo CSV
        nombre_csv = "datos_banxico.csv"
        df.to_csv(nombre_csv, index=False)
        logging.info(f"Datos guardados en {nombre_csv}")
        
        # Guardar en archivo Excel
        nombre_excel = "datos_banxico.xlsx"
        df.to_excel(nombre_excel, index=False)
        logging.info(f"Datos guardados en {nombre_excel}")
    else:
        logging.warning("No hay datos disponibles.")

if __name__ == '__main__':
    main()

