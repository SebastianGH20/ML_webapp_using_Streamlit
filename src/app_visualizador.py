import streamlit as st
import pandas as pd
import plotly.express as px

# Título de la aplicación
st.title('Análisis del Dataset de Anime')

# Subtítulo
st.header('Visualización de Datos del Dataset de Anime')

# Cargar los datos
@st.cache_data
def load_data():
    data = pd.read_csv('anime.csv')  # Asegúrate de que el archivo anime.csv esté en el mismo directorio
    return data

data = load_data()

# Verificar los nombres de las columnas
st.write("Columnas del DataFrame:")
st.write(data.columns)

# Mostrar el DataFrame
st.write("Aquí están los datos del dataset de anime:")
st.write(data)

# Asegurarse de que la columna 'rating' existe (ajusta según tu interés)
if 'rating' not in data.columns:
    st.error("La columna 'rating' no se encuentra en el DataFrame.")
else:
    # Crear un gráfico de líneas con los datos
    st.header('Gráfico de líneas de los ratings')
    st.line_chart(data['rating'].dropna())  # Asegúrate de eliminar NaN si es necesario

    # Slider para seleccionar un valor de rating
    valor_seleccionado = st.slider('Selecciona un valor de rating', 0.0, 10.0, float(data['rating'].mean()))
    st.write('Valor seleccionado:', valor_seleccionado)

    # Crear un filtro en el DataFrame basado en el rating seleccionado
    filtered_data = data[data['rating'] <= valor_seleccionado]

    # Mostrar el DataFrame filtrado
    st.write("Datos filtrados hasta el rating seleccionado:")
    st.write(filtered_data)

    # Crear un gráfico de barras con los datos filtrados
    st.header('Gráfico de barras de los ratings filtrados')
    st.bar_chart(filtered_data['rating'].value_counts())

    # Visualización adicional con Plotly (opcional)
    st.header('Distribución de géneros en los datos filtrados')
    if 'genre' in filtered_data.columns:
        genres = filtered_data['genre'].str.get_dummies(sep=', ')  # Convertir la columna de géneros en dummies
        genres_sum = genres.sum().reset_index()
        genres_sum.columns = ['Genre', 'Count']

        fig = px.bar(genres_sum, x='Genre', y='Count', title='Distribución de Géneros en los Datos Filtrados')
        st.plotly_chart(fig)
    else:
        st.error("La columna 'genre' no se encuentra en el DataFrame.")
