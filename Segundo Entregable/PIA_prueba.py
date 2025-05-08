import requests
import re
from datetime import datetime
from collections import Counter

# Función para validar fecha
def es_fecha_valida(fecha):
    try:
        datetime.strptime(fecha, "%Y-%m-%d")
        return True
    except ValueError:
        return False

while True:
    # Pedir país
    pais = input("¿Qué país/ciudad deseas consultar?(Nombre en ingles) ").strip().lower()

    # Pedir y validar fecha de inicio
    fecha_inicio = input("Fecha de inicio (YYYY-MM-DD): ").strip()
    while not es_fecha_valida(fecha_inicio):
        print("Fecha no válida.")
        fecha_inicio = input("Ingresa la fecha de inicio nuevamente (YYYY-MM-DD): ").strip()

    # Pedir y validar fecha de fin
    fecha_fin = input("Fecha de fin (YYYY-MM-DD): ").strip()
    while not es_fecha_valida(fecha_fin):
        print("Fecha no válida.")
        fecha_fin = input("Ingresa la fecha de fin nuevamente (YYYY-MM-DD): ").strip()

    url = "https://earthquake.usgs.gov/fdsnws/event/1/query"
    params = {
        "format": "geojson",
        "starttime": fecha_inicio,
        "endtime": fecha_fin,
        "limit": 20000
    }

    # Hacer solicitud
    respuesta = requests.get(url, params=params)

    # Procesar respuesta
    if respuesta.status_code == 200:
        datos = respuesta.json()
        total = 0
        magnitudes = []

        patron = re.compile(rf"\b{re.escape(pais)}\b")  # Expresión regular para coincidencia exacta

        for eq in datos['features']:
            lugar = eq['properties']['place'].lower()
            magnitud = eq['properties']['mag']

            if patron.search(lugar):
                total += 1
                magnitudes.append(round(magnitud, 1))

        # Guardar resultados en archivo
        with open("resultado_terremotos.txt", "a", encoding="utf-8") as archivo:
            archivo.write(f"\nConsulta para '{pais}' del {fecha_inicio} al {fecha_fin}:\n")

            if total > 0:
                print(f"\nTotal de terremotos en {pais}: {total}")
                print("Cantidad por magnitud:")
                archivo.write(f"Total de terremotos en {pais}: {total}\n")
                archivo.write("Cantidad por magnitud:\n")
                for mag, cantidad in sorted(Counter(magnitudes).items()):
                    print(f" - Magnitud {mag}: {cantidad}")
                    archivo.write(f" - Magnitud {mag}: {cantidad}\n")
            else:
                print(f"No se encontraron terremotos en {pais}.")
                print("Verifica que el nombre esté escrito correctamente.")
                archivo.write(f"No se encontraron terremotos en {pais}.\n")
                archivo.write("Verifica que el nombre esté escrito correctamente.\n")
    else:
        print("Error al conectar con la API.")

    # Preguntar si desea hacer otra consulta
    otra = input("\n¿Deseas consultar otro país? (s/n): ").strip().lower()
    if otra != 's':
        print("Programa finalizado.")
        break
