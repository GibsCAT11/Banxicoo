import requests
import pandas as pd
from datetime import datetime

def obtener_datos_banxico(token, serie, fecha_inicio, fecha_fin):
    url = f"https://www.banxico.org.mx/SieAPIRest/service/v1/series/{serie}/datos/{fecha_inicio}/{fecha_fin}"
    headers = {"Bmx-Token": token}
    
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        datos = response.json()
        # Extraemos los datos de la serie
        serie_datos = datos['bmx']['series'][0]['datos']
        return serie_datos
    else:
        print("Error al obtener datos:", response.status_code, response.text)
        return []

# Configuración del servicio
token = "398cd10afbbafa93ccbbc962ecfd7ab72c3edb07b4bb4938b833e3a244baf196"  # Reemplaza con tu token real
serie = "SF43718"        # Serie de ejemplo
fecha_inicio = "2015-01-01"
fecha_fin = datetime.now().strftime("%Y-%m-%d")  # Fecha actual

# Obtener los datos de Banxico
datos = obtener_datos_banxico(token, serie, fecha_inicio, fecha_fin)

if datos:
    # Crear un DataFrame para mostrar los datos en tabla
    df = pd.DataFrame(datos)
    print(df)
    
    # Guardar en archivo CSV (documento de texto)
    nombre_csv = "datos_banxico.csv"
    df.to_csv(nombre_csv, index=False)
    print(f"Datos guardados en {nombre_csv}")
    
    # Guardar en archivo Excel
    nombre_excel = "datos_banxico.xlsx"
    df.to_excel(nombre_excel, index=False)
    print(f"Datos guardados en {nombre_excel}")
else:
    print("No hay datos disponibles.")
