import pandas as pd
from typing import List

# Definición de Constantes de Archivo
ARCHIVO_UF1 = "Notas_Alumnos_UF1.csv"
ARCHIVO_UF2 = "Notas_Alumnos_UF2.csv"

def cargar_y_combinar_datos(archivo1: str, archivo2: str) -> pd.DataFrame:
    """Carga los datos de las UF y los combina en un único DataFrame."""
    try:
        # Cargar los DataFrames ESPECIFICANDO la codificación como 'latin1'
        # para manejar caracteres como la 'ó' (la causa del byte 0xf3).
        df_uf1 = pd.read_csv(archivo1, sep=";", encoding='latin1')
        df_uf2 = pd.read_csv(archivo2, sep=";", encoding='latin1')
        
        # Unir por las columnas comunes: 'Id', 'Apellidos', y 'Nombre'
        df_combinado = pd.merge(df_uf1, df_uf2, on=['Id', 'Apellidos', 'Nombre'], how='inner')
        
        print("✅ Datos de UF1 y UF2 cargados y combinados correctamente.")
        return df_combinado
        
    except FileNotFoundError:
        print("❌ Error: Uno o ambos archivos CSV no fueron encontrados.")
        return pd.DataFrame()
    except Exception as e:
        # Mantén el manejo de otros errores
        print(f"❌ Ocurrió un error al cargar o combinar los datos: {e}")
        return pd.DataFrame()
def analizar_rendimiento_extremo(df: pd.DataFrame, nota_uf1: int, nota_uf2: int) -> pd.DataFrame:
    """Filtra y devuelve a los estudiantes con notas específicas en ambas UF."""
    if df.empty:
        return pd.DataFrame()

    print(f"\n--- Alumnos con UF1={nota_uf1} y UF2={nota_uf2} ---")
    
    # Aplicar el filtro:
    filtro = (df['UF1'] == nota_uf1) & (df['UF2'] == nota_uf2)
    
    # Seleccionar solo las columnas de identificación para el resultado
    resultado = df[filtro][['Apellidos', 'Nombre']]
    
    return resultado

def calcular_y_mostrar_medias(df: pd.DataFrame):
    """Calcula e imprime la nota media simple de las dos UF."""
    if df.empty:
        return
    
    # Calcular la media simple de las dos UF
    df['Media_UF1_UF2'] = (df['UF1'] + df['UF2']) / 2
    
    print("\n--- Medias Generales ---")
    print(f"Nota Media de UF1: {df['UF1'].mean():.2f}")
    print(f"Nota Media de UF2: {df['UF2'].mean():.2f}")
    print(f"Nota Media Global (UF1 y UF2): {df['Media_UF1_UF2'].mean():.2f}")
    
    # Opcional: Mostrar los 5 mejores por media
    print("\n--- Top 5 Estudiantes por Media ---")
    top_5 = df.sort_values(by='Media_UF1_UF2', ascending=False).head(5)
    print(top_5[['Apellidos', 'Nombre', 'UF1', 'UF2', 'Media_UF1_UF2']].to_string(index=False))


# --- Punto de Ejecución Principal ---
if __name__ == "__main__":
    # 1. Cargar y combinar los datos
    datos_combinados = cargar_y_combinar_datos(ARCHIVO_UF1, ARCHIVO_UF2)
    
    if not datos_combinados.empty:
        # 2. Análisis del rendimiento extremo (la consulta original)
        # Buscar alumnos con 0 en UF1 y 10 en UF2
        alumnos_interes = analizar_rendimiento_extremo(datos_combinados, nota_uf1=0, nota_uf2=10)
        
        if not alumnos_interes.empty:
            print(f"Se encontraron {len(alumnos_interes)} alumnos con UF1=0 y UF2=10:")
            print(alumnos_interes.to_string(index=False))
        else:
            print("No se encontraron alumnos con esa combinación de notas.")

        # 3. Análisis general de medias
        calcular_y_mostrar_medias(datos_combinados)