import re
import numpy as np
import statistics
from collections import defaultdict

archivo = "resultado_terremotos.txt"

#Expresiones regulares
patron_consulta = re.compile(r"Consulta para '(.+?)' del (\d{4}-\d{2}-\d{2}) al (\d{4}-\d{2}-\d{2}):")
patron_magnitud = re.compile(r"- Magnitud ([\d.]+): (\d+)")

#Lista estructurada para todos los datos
datos_estructurados = []

#Variables temporales
region_actual = None
fecha_inicio = None
fecha_fin = None
magnitudes_actuales = []

with open(archivo, "r", encoding="utf-8") as f:
    for linea in f:
        linea = linea.strip()

        #Si encontramos una nueva consulta (región + fechas)
        match_consulta = patron_consulta.match(linea)
        if match_consulta:
            #Si ya había una región en curso, guardamos sus datos antes de continuar
            if region_actual and magnitudes_actuales:
                try:
                    moda = statistics.mode(magnitudes_actuales)
                except statistics.StatisticsError:
                    moda = None  #No hay una sola moda

                datos_estructurados.append({
                    "region": region_actual,
                    "fecha_inicio": fecha_inicio,
                    "fecha_fin": fecha_fin,
                    "magnitudes": magnitudes_actuales,
                    "frecuencia": dict(sorted(
                        {m: magnitudes_actuales.count(m) for m in set(magnitudes_actuales)}.items())),
                    "media": round(np.mean(magnitudes_actuales), 2),
                    "moda": moda
                })

            #Inicializamos nueva región
            region_actual = match_consulta.group(1).lower()
            fecha_inicio = match_consulta.group(2)
            fecha_fin = match_consulta.group(3)
            magnitudes_actuales = []
            continue

        #Si encontramos una línea de magnitud
        match_magnitud = patron_magnitud.match(linea)
        if match_magnitud:
            magnitud = float(match_magnitud.group(1))
            cantidad = int(match_magnitud.group(2))
            magnitudes_actuales.extend([magnitud] * cantidad)

#Guardar última región
if region_actual and magnitudes_actuales:
    try:
        moda = statistics.mode(magnitudes_actuales)
    except statistics.StatisticsError:
        moda = None

    datos_estructurados.append({
        "region": region_actual,
        "fecha_inicio": fecha_inicio,
        "fecha_fin": fecha_fin,
        "magnitudes": magnitudes_actuales,
        "frecuencia": dict(sorted(
            {m: magnitudes_actuales.count(m) for m in set(magnitudes_actuales)}.items())),
        "media": round(np.mean(magnitudes_actuales), 2),
        "moda": moda
    })

#Mostrar resumen organizado (sin graficar)
for entrada in datos_estructurados:
    print(f"\nRegión: {entrada['region']}")
    print(f"Fechas: {entrada['fecha_inicio']} a {entrada['fecha_fin']}")
    print(f"Media: {entrada['media']}")
    print(f"Moda: {entrada['moda']}")
    print(f"Frecuencia por magnitud:")
    for mag, freq in entrada["frecuencia"].items():
        print(f"    - {mag}: {freq}")
