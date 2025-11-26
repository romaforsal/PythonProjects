import requests
import xml.etree.ElementTree as ET
import streamlit as st


# - LÓGICA DE DATOS -

def obtener_datos_bce():
    url = "https://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml"

    try:
        # Requisito: Petición HTTP GET
        response = requests.get(url)

        if response.status_code == 200:
            # Requisito: Parsear estructura XML
            # Usamos fromstring para convertir el texto en un objeto XML
            root = ET.fromstring(response.content)

            # Espacio de nombres (Namespace) que aparece en el XML
            # A veces es necesario para encontrar las etiquetas, pero aquí buscaremos
            # iterando para hacerlo más sencillo.

            datos_monedas = {'EUR': 1.0}  # Requisito: Añadir Euro manualmente
            fecha_actualizacion = "Desconocida"

            # Recorremos los nodos 'Cube'. La estructura es anidada.
            # Buscamos todos los elementos iterando el árbol
            for child in root.iter():
                # Extraer fecha
                if 'time' in child.attrib:
                    fecha_actualizacion = child.attrib['time']

                # Extraer monedas y tasas
                if 'currency' in child.attrib and 'rate' in child.attrib:
                    moneda = child.attrib['currency']
                    # Convertimos la tasa a float para poder calcular
                    tasa = float(child.attrib['rate'])
                    datos_monedas[moneda] = tasa

            return True, fecha_actualizacion, datos_monedas
        else:
            return False, None, None

    except Exception as e:
        return False, str(e), None


# - INTERFAZ GRÁFICA -

def main():
    # Título de la aplicación
    st.title("Conversor de Divisas (BCE)")
    st.write("Esta aplicación consume XML en tiempo real del Banco Central Europeo.")

    # Requisito: Carga Automática al iniciar
    exito, fecha, tasas = obtener_datos_bce()

    if exito:
        # Requisito: Mostrar fecha de actualización
        st.success(f"Datos cargados. Fecha oficial: {fecha}")

        # Mostrar datos crudos si el usuario quiere (como en la imagen)
        with st.expander("Ver tasas de cambio"):
            st.write(tasas)

        # - SECCIÓN DE ENTRADA DE DATOS -
        col1, col2, col3 = st.columns(3)

        with col1:
            # Requisito: Campo numérico para cantidad
            # Streamlit maneja la validación numérica automáticamente aquí
            cantidad = st.number_input("Cantidad", min_value=0.0, value=100.0, step=10.0)

        monedas_disponibles = list(tasas.keys())

        with col2:
            # Requisito: Desplegable Moneda Origen
            origen = st.selectbox("De:", monedas_disponibles, index=monedas_disponibles.index('EUR'))

        with col3:
            # Requisito: Desplegable Moneda Destino
            destino = st.selectbox("A:", monedas_disponibles, index=monedas_disponibles.index('USD'))

        # - CÁLCULO Y RESULTADO -

        # Requisito: Botón para calcular
        if st.button("Calcular Conversión"):
            # Lógica de conversión cruzada
            tasa_origen = tasas[origen]
            tasa_destino = tasas[destino]

            resultado = (cantidad / tasa_origen) * tasa_destino

            # Requisito: Mostrar resultado final
            st.metric(label=f"Valor en {destino}", value=f"{resultado:.2f} {destino}")

            # Extra: Mostrar la tasa de cambio implícita
            st.caption(f"Tipo de cambio utilizado: 1 {origen} = {(1 / tasa_origen) * tasa_destino:.4f} {destino}")

    else:
        st.error("Error al conectar con el servidor del BCE.")
        if fecha:  # En este caso 'fecha' contiene el mensaje de error
            st.write(fecha)


if __name__ == "__main__":
    main()