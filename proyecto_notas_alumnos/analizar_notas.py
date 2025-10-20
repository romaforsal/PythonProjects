import csv
from typing import List, Dict, Any

# Definición de Constantes de Archivo
ARCHIVO_UF1 = "Notas_Alumnos_UF1.csv"
ARCHIVO_UF2 = "Notas_Alumnos_UF2.csv"
ARCHIVO_SALIDA = "Notas_Combinadas.csv"
DELIMITADOR = ";"
CODIFICACION = 'latin1'  # Necesario por el error de codificación


def cargar_y_combinar_datos(archivo1: str, archivo2: str) -> List[Dict[str, Any]]:
    """
    Carga los datos de las UF usando DictReader y los combina por 'Id'.
    Calcula la media de las dos UF en el proceso.
    """
    try:
        # 1. Cargar datos de UF1 en un diccionario de apoyo (key=Id)
        uf_data_map = {}
        with open(archivo1, mode='r', encoding=CODIFICACION, newline='') as f1:
            reader1 = csv.DictReader(f1, delimiter=DELIMITADOR)
            for row in reader1:
                # Convertir Id y UF1 a enteros para cálculos futuros
                row['Id'] = int(row['Id'])
                row['UF1'] = int(row['UF1'])
                uf_data_map[row['Id']] = row

        # 2. Combinar con datos de UF2
        with open(archivo2, mode='r', encoding=CODIFICACION, newline='') as f2:
            reader2 = csv.DictReader(f2, delimiter=DELIMITADOR)
            for row in reader2:
                # Convertir Id y UF2 a enteros
                row['Id'] = int(row['Id'])
                row['UF2'] = int(row['UF2'])

                # Encontrar la fila correspondiente en el mapa de UF1 y añadir UF2
                if row['Id'] in uf_data_map:
                    combined_row = uf_data_map[row['Id']]
                    combined_row['UF2'] = row['UF2']

                    # 3. Calcular la media al combinar
                    combined_row['Media_UF1_UF2'] = (combined_row['UF1'] + combined_row['UF2']) / 2

        print("✅ Datos de UF1 y UF2 cargados y combinados correctamente.")
        # Devolver la lista de diccionarios (valores del mapa)
        return list(uf_data_map.values())

    except FileNotFoundError:
        print("❌ Error: Uno o ambos archivos CSV no fueron encontrados.")
        return []
    except Exception as e:
        print(f"❌ Ocurrió un error al cargar o combinar los datos: {e}")
        return []


def analizar_rendimiento_extremo(datos: List[Dict[str, Any]], nota_uf1: int, nota_uf2: int) -> List[Dict[str, Any]]:
    """Filtra y devuelve a los estudiantes con notas específicas en ambas UF."""
    if not datos:
        return []

    print(f"\n--- Alumnos con UF1={nota_uf1} y UF2={nota_uf2} ---")

    # Aplicar el filtro usando una lista de comprensión
    resultado = [
        estudiante for estudiante in datos
        if estudiante.get('UF1') == nota_uf1 and estudiante.get('UF2') == nota_uf2
    ]

    # Seleccionar solo las columnas de identificación para la salida impresa
    return [{'Apellidos': e['Apellidos'], 'Nombre': e['Nombre']} for e in resultado]


def calcular_y_mostrar_medias(datos: List[Dict[str, Any]]):
    """Calcula e imprime la nota media de las dos UF."""
    if not datos:
        return

    # Calcular medias generales
    medias_uf1 = [d['UF1'] for d in datos]
    medias_uf2 = [d['UF2'] for d in datos]

    media_total_uf1 = sum(medias_uf1) / len(medias_uf1)
    media_total_uf2 = sum(medias_uf2) / len(medias_uf2)
    media_global = (media_total_uf1 + media_total_uf2) / 2

    print("\n--- Medias Generales ---")
    print(f"Nota Media de UF1: {media_total_uf1:.2f}")
    print(f"Nota Media de UF2: {media_total_uf2:.2f}")
    print(f"Nota Media Global (UF1 y UF2): {media_global:.2f}")

    # Ordenar y mostrar Top 5
    datos_ordenados = sorted(datos, key=lambda x: x['Media_UF1_UF2'], reverse=True)

    print("\n--- Top 5 Estudiantes por Media ---")
    for i, estudiante in enumerate(datos_ordenados[:5]):
        print(
            f"{estudiante['Apellidos']:<20} {estudiante['Nombre']:<15} UF1: {estudiante['UF1']:<2} UF2: {estudiante['UF2']:<2} Media: {estudiante['Media_UF1_UF2']:.2f}")


def escribir_datos_combinados(datos: List[Dict[str, Any]], archivo_salida: str):
    """Escribe la lista de diccionarios combinada en un nuevo CSV usando DictWriter."""
    if not datos:
        print("No hay datos para escribir.")
        return

    # Definir los nombres de las columnas para el archivo de salida
    fieldnames = ['Id', 'Apellidos', 'Nombre', 'UF1', 'UF2', 'Media_UF1_UF2']

    try:
        with open(archivo_salida, mode='w', encoding=CODIFICACION, newline='') as outfile:
            # Crear el objeto DictWriter
            writer = csv.DictWriter(outfile, fieldnames=fieldnames, delimiter=DELIMITADOR)

            # Escribir la cabecera
            writer.writeheader()

            # Escribir las filas
            writer.writerows(datos)

        print(f"\n✅ Archivo de salida '{archivo_salida}' creado con éxito usando DictWriter.")
    except Exception as e:
        print(f"❌ Error al escribir el archivo con DictWriter: {e}")


# --- Punto de Ejecución Principal ---
if __name__ == '__main__':
    # 1. Cargar, combinar y calcular medias
    datos_combinados = cargar_y_combinar_datos(ARCHIVO_UF1, ARCHIVO_UF2)

    if datos_combinados:
        # 2. Análisis del rendimiento extremo (consulta original: 0 en UF1 y 10 en UF2)
        alumnos_interes = analizar_rendimiento_extremo(datos_combinados, nota_uf1=0, nota_uf2=10)

        if alumnos_interes:
            print(f"Se encontraron {len(alumnos_interes)} alumnos con UF1=0 y UF2=10:")
            # Imprimir en formato simple de tabla
            for alumno in alumnos_interes:
                print(f"  {alumno['Apellidos']}, {alumno['Nombre']}")
        else:
            print("No se encontraron alumnos con esa combinación de notas.")

        # 3. Análisis general de medias
        calcular_y_mostrar_medias(datos_combinados)

        # 4. Escribir el resultado combinado a un nuevo CSV usando DictWriter
        escribir_datos_combinados(datos_combinados, ARCHIVO_SALIDA)