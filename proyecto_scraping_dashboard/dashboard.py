import streamlit as st
import pandas as pd
import altair as alt

# --- Configuración de la página ---
st.set_page_config(
    page_title="Dashboard de Libros Scrapeados",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Título principal ---
st.title("📚 Dashboard Interactivo de Libros")
st.markdown("Explora los datos de libros extraídos de **https://books.toscrape.com/**")

# --- Cargar datos ---
@st.cache_data
def load_data(file_path):
    """Carga los datos del archivo CSV."""
    df = pd.read_csv(file_path, encoding='utf-8-sig')
    return df

try:
    df = load_data('proyecto_scraping_dashboard/books_data.csv')
    df_original = df.copy()
except FileNotFoundError:
    st.error("❌ Archivo 'books_data.csv' no encontrado. Asegúrate de haber ejecutado el script de scraping primero.")
    st.stop()

# --- Sidebar para Filtros Interactivos ---
st.sidebar.header("⚙️ Filtros de Datos")

# 1. Filtro por Rating (Categoría/Distribución)
min_rating = st.sidebar.slider(
    "Filtrar por Rating (mínimo):",
    min_value=1,
    max_value=5,
    value=3
)

# 2. Filtro por Precio (Rango)
price_min, price_max = st.sidebar.slider(
    "Filtrar por Rango de Precio (£):",
    min_value=float(df_original['Precio (£)'].min()),
    max_value=float(df_original['Precio (£)'].max()),
    value=(float(df_original['Precio (£)'].min()), float(df_original['Precio (£)'].max()))
)

# --- Aplicar Filtros ---
df_filtrado = df_original[
    (df_original['Rating (1-5)'] >= min_rating) &
    (df_original['Precio (£)'] >= price_min) &
    (df_original['Precio (£)'] <= price_max)
]

# --- Resultados del Filtrado ---
st.subheader(f"Resultados ({len(df_filtrado)} libros encontrados)")
if df_filtrado.empty:
    st.warning("No hay libros que coincidan con los filtros seleccionados.")
else:
    # 3. Visualización de la Tabla Interactiva con la columna de imagen
    st.dataframe(
        df_filtrado,
        width='stretch', # Usa 'stretch' para que se expanda. (Actualización por el warning anterior)
        hide_index=True,
        column_order=['Imagen', 'Título', 'Precio (£)', 'Rating (1-5)'], # Reordenar para que Imagen salga primero
        column_config={
            "Imagen": st.column_config.ImageColumn(
                "Portada", # Etiqueta que aparecerá en la columna
                help="Imagen de la portada del libro"
            ),
            # Puedes configurar otras columnas aquí si quieres, por ejemplo:
            "Precio (£)": st.column_config.NumberColumn(
                "Precio (€)",
                format="£ %.2f", # Formato de moneda
                help="Precio del libro en Libras"
            ),
            "Rating (1-5)": st.column_config.NumberColumn(
                "Rating",
                format="%d ⭐", # Añadir estrellas al rating
                help="Puntuación del libro de 1 a 5 estrellas"
            )
        }
    )

    st.markdown("---")

    # --- 4. Representación Gráfica ---

    # Gráfico 1: Distribución de Ratings (Gráfico de Barras)
    st.subheader("Gráfico: Distribución de Libros por Rating (1-5)")

    rating_counts = df_filtrado.groupby('Rating (1-5)').size().reset_index(name='Cantidad de Libros')

    chart_ratings = alt.Chart(rating_counts).mark_bar().encode(
        x=alt.X('Rating (1-5):O', title="Rating"),
        y=alt.Y('Cantidad de Libros', title="Número de Libros"),
        tooltip=['Rating (1-5)', 'Cantidad de Libros'],
        color=alt.Color('Rating (1-5):O', scale=alt.Scale(range=['red', 'orange', 'yellow', 'lightgreen', 'green']))
    ).properties(
        title='Distribución de Ratings en el Conjunto Filtrado'
    ).interactive()

    st.altair_chart(chart_ratings, use_container_width=True)

    st.markdown("---")

    # Gráfico 2: Precio vs. Rating (Relación interesante)
    st.subheader("Gráfico de Dispersión: Precio vs. Rating")

    chart_scatter = alt.Chart(df_filtrado).mark_circle(size=60).encode(
        x=alt.X('Precio (£)', title='Precio en Libras (£)'),
        y=alt.Y('Rating (1-5)', title='Rating (1-5)', scale=alt.Scale(domain=[0.5, 5.5])),
        color='Rating (1-5):O',
        tooltip=['Título', 'Precio (£)', 'Rating (1-5)']
    ).properties(
        title='Precio de Libros por Nivel de Rating'
    ).interactive()

    st.altair_chart(chart_scatter, use_container_width=True)