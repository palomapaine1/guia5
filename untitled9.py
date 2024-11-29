# -*- coding: utf-8 -*-
"""Untitled9.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1cmQo4Pxl-HcJtzd7bNayItbiiC3_tzFM
"""

import pandas as pd
import requests
import streamlit as st

# Título de la aplicación
st.title('Aplicación Web: Datos desde una API REST')
# URL de la API REST (puedes cambiarla por cualquier API pública que devuelva JSON)
api_url = 'https://jsonplaceholder.typicode.com/posts'
# Realizar la petición a la API
response = requests.get(api_url)
# Verificar que la respuesta sea exitosa (código 200)
if response.status_code == 200:
    # Convertir los datos JSON en un DataFrame de Pandas
    data = response.json()
    df = pd.DataFrame(data)
    # Mostrar los primeros registros
    st.write('Datos obtenidos de la API:')
    st.write(df.head())
else:
    st.error('Error al obtener los datos de la API')

if df is not None and not df.empty:
    # Verifica si las columnas necesarias existen
    if 'name' in df.columns:
        df['Nombre'] = df['name'].apply(lambda x: x.get('common') if isinstance(x, dict) else None)
    else:
        df['Nombre'] = None

    if 'region' in df.columns:
        df['Región'] = df['region']
    else:
        df['Región'] = None

    if 'population' in df.columns:
        df['Población'] = df['population']
    else:
        df['Población'] = None

    if 'area' in df.columns:
        df['Área (km²)'] = df['area']
    else:
        df['Área (km²)'] = None

    if 'borders' in df.columns:
        df['Fronteras'] = df['borders'].apply(lambda x: len(x) if isinstance(x, list) else 0)
    else:
        df['Fronteras'] = 0

    if 'languages' in df.columns:
        df['Idiomas Oficiales'] = df['languages'].apply(lambda x: len(x) if isinstance(x, dict) else 0)
    else:
        df['Idiomas Oficiales'] = 0

    if 'timezones' in df.columns:
        df['Zonas Horarias'] = df['timezones'].apply(lambda x: len(x) if isinstance(x, list) else 0)
    else:
        df['Zonas Horarias'] = 0

    st.write("Transformación exitosa:")
    st.write(df.head())
    # Filtrar columnas seleccionadas
    columnas = ['Nombre', 'Región', 'Población', 'Área (km²)', 'Fronteras', 'Idiomas Oficiales', 'Zonas Horarias']
    df_cleaned = df[columnas]

    # Mostrar DataFrame con las columnas seleccionadas
    st.title("Interacción con los datos:")
    st.write("Mostrar datos originales:")
    st.dataframe(df_cleaned)

    # Selección de columnas
    columnas = ['Nombre', 'Región', 'Población', 'Área (km²)', 'Fronteras', 'Idiomas Oficiales', 'Zonas Horarias']
    columnas_presentes = [col for col in columnas if col in df.columns]
    df_cleaned = df[columnas_presentes]
    st.write("DataFrame final para trabajar:")
    st.write(df_cleaned)
else:
    st.error("El DataFrame está vacío o no es válido.")
     # Mostrar DataFrame con las columnas seleccionadas
    st.title("Interacción con los datos")
    st.header("Mostrar los datos originales")
    st.dataframe(df_cleaned)
    data = {
    "Nombre": ["País A", "País B", "País C", "País D"],
    "Población": [5000000, 12000000, 8000000, 6000000],
    "Área (km²)": [100000, 250000, 180000, 150000],
    "Zonas Horarias": [1, 2, 1, 3],
    "Región": ["Asia", "Europa", "África", "América"]}
df = pd.DataFrame(data)

# Título de la aplicación
st.title("Cálculo de Estadísticas con Selección por Categoría")

# Mostrar el DataFrame original
st.subheader("Datos Originales")
st.write(df)

# Selección de categoría
st.subheader("Selección por Categoría")
categorias = {"Demografía": ["Población", "Zonas Horarias"], 
              "Geografía": ["Área (km²)"]}

# Botón para mostrar opciones de categoría
if st.button("Seleccionar Categoría"):
    categoria = st.radio("Elige una categoría:", list(categorias.keys()))

    if categoria:
        columna_seleccionada = st.selectbox(
            f"Seleccione una columna dentro de la categoría '{categoria}':",
            categorias[categoria])

        if columna_seleccionada:
            # Cálculos estadísticos
            media = df[columna_seleccionada].mean()
            mediana = df[columna_seleccionada].median()
            desviacion = df[columna_seleccionada].std()

            # Mostrar resultados
            st.write(f"**Columna seleccionada:** {columna_seleccionada}")
            st.write(f"**Media:** {media}")
            st.write(f"**Mediana:** {mediana}")
            st.write(f"**Desviación estándar:** {desviacion}")


    # Mostrar el DataFrame ordenado
    st.write('DataFrame Ordenado:')
    st.write(df_ordenado)
    st.subheader("Filtrar Datos")
    columna_filtro = st.selectbox("Selecciona una columna para filtrar:", df.select_dtypes(include=['number']).columns)
    if columna_filtro:
     min_val, max_val = st.slider(
        f"Selecciona el rango para {columna_filtro}:",
        float(df[columna_filtro].min()),
        float(df[columna_filtro].max()),
        (float(df[columna_filtro].min()), float(df[columna_filtro].max())))
    df_filtrado = df[(df[columna_filtro] >= min_val) & (df[columna_filtro] <= max_val)]
    st.write("**Datos Filtrados:**")
    st.write(df_filtrado)
    # Botón para descargar los datos filtrados
    st.subheader("Exportar Datos Filtrados")
    formato = st.radio("Elige el formato para descargar:", ('CSV', 'Excel'))

    @st.cache_data
    def convertir_a_csv(df):
        return df.to_csv(index=False).encode('utf-8')

    @st.cache_data
    def convertir_a_excel(df):
        import io
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name='DatosFiltrados')
            writer.save()
        return buffer.getvalue()

    if formato == 'CSV':
        st.download_button(
            label="Descargar en CSV",
            data=convertir_a_csv(df_filtrado),
            file_name='datos_filtrados.csv',
            mime='text/csv')
    else:
        st.download_button(
            label="Descargar en Excel",
            data=convertir_a_excel(df_filtrado),
            file_name='datos_filtrados.xlsx',
            mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    # Título de la aplicación
st.title("Gráficos Interactivos con Streamlit")

# Cargar archivo o usar ejemplo
st.subheader("Carga de Datos")
uploaded_file = st.file_uploader("Sube un archivo CSV o Excel:", type=["csv", "xlsx"])

if uploaded_file:
    try:
        # Detectar formato y cargar archivo
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        elif uploaded_file.name.endswith('.xlsx'):
            df = pd.read_excel(uploaded_file)
        st.success("Archivo cargado exitosamente.")
    except Exception as e:
        st.error(f"Error al cargar el archivo: {e}")
        df = pd.DataFrame()
else:
    # Crear un DataFrame de ejemplo si no se sube archivo
    st.info("Usando datos de ejemplo porque no se subió archivo.")
    data = {'Categoría': ['A', 'B', 'C', 'D', 'E'],'Valor 1': [10, 20, 30, 40, 50],'Valor 2': [15, 25, 35, 45, 55],'Valor 3': [5, 15, 25, 35, 45],}
    df = pd.DataFrame(data)

# Verificar si el DataFrame tiene datos
if df.empty:
    st.error("No hay datos disponibles. Sube un archivo para continuar.")
else:
    # Mostrar los datos originales
    st.subheader("Datos Originales")
    st.write(df)

    # Sección de gráficos interactivos
    st.subheader("Gráficos Interactivos")

    # Selección de tipo de gráfico
    tipo_grafico = st.selectbox("Selecciona el tipo de gráfico:",
                                ["Dispersión", "Línea", "Barras", "Histograma", "Pastel"])

    # Selección de variables
    columnas_numericas = df.select_dtypes(include=['number']).columns
    if len(columnas_numericas) > 0:
        columna_x = st.selectbox("Selecciona la columna para el eje X:", columnas_numericas)
        columna_y = st.selectbox("Selecciona la columna para el eje Y:", columnas_numericas)

        # Ajuste de rango para los ejes
        st.subheader("Ajustar Rango de los Ejes")
        rango_x = st.slider("Rango del eje X:",
                            float(df[columna_x].min()),
                            float(df[columna_x].max()),
                            (float(df[columna_x].min()), float(df[columna_x].max())))
        rango_y = st.slider("Rango del eje Y:",
                            float(df[columna_y].min()),
                            float(df[columna_y].max()),
                            (float(df[columna_y].min()), float(df[columna_y].max())))

        # Crear gráfico
        fig, ax = plt.subplots()
        if tipo_grafico == "Dispersión":
            ax.scatter(df[columna_x], df[columna_y], color='blue', alpha=0.7)
        elif tipo_grafico == "Línea":
            ax.plot(df[columna_x], df[columna_y], color='green', marker='o')
        elif tipo_grafico == "Barras":
            ax.bar(df[columna_x], df[columna_y], color='orange', alpha=0.7)
        elif tipo_grafico == "Histograma":
            ax.hist(df[columna_x], bins=10, color='purple', alpha=0.7)
            ax.set_ylabel("Frecuencia")
        elif tipo_grafico == "Pastel":
            if len(df[columna_x].unique()) <= 10:
                ax.pie(df[columna_y], labels=df[columna_x], autopct='%1.1f%%')
                ax.set_aspect('equal')
            else:
                st.warning("El gráfico de pastel requiere menos de 10 categorías únicas en el eje X.")
                st.stop()

        # Ajustar límites
        ax.set_xlim(rango_x)
        ax.set_ylim(rango_y)

        # Etiquetas y título
        if tipo_grafico != "Pastel":
            ax.set_title(f"{tipo_grafico}: {columna_y} vs {columna_x}")
            ax.set_xlabel(columna_x)
            ax.set_ylabel(columna_y)

        # Mostrar gráfico
        st.pyplot(fig)

        # Descargar gráfico en PNG
        st.subheader("Descargar Gráfico")
        buffer = io.BytesIO()
        fig.savefig(buffer, format='png')
        buffer.seek(0)
        st.download_button(
            label="Descargar gráfico como PNG",
            data=buffer,
            file_name="grafico.png",
            mime="image/png" )
    else:
        st.warning("El DataFrame no contiene columnas numéricas para generar gráficos.")





 
