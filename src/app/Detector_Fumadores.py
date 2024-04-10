import streamlit as st
import pandas as pd
import joblib
from sklearn.preprocessing import StandardScaler

# Cargar el modelo y el scaler previamente entrenados
mejor_forest = joblib.load('src/model/random_forest_model.joblib')
scaler = joblib.load('src/model/scaler.joblib')

# Personalización del favicon y la imagen de la app
st.set_page_config(page_title='Detector de Fumadores', page_icon='🚬', layout='centered', initial_sidebar_state='expanded')

# Título y descripción de la aplicación
st.title('Detector de Fumadores')
st.write('Esta aplicación predice si una persona es fumadora basada en sus biomarcadores y otras características de salud.')

# Cargar y mostrar una imagen (ajusta la ruta de la imagen)
st.image('src/app/Portada.png', caption='Detector de Fumadores', use_column_width=True)

# Subir archivo CSV
uploaded_file = st.file_uploader("Sube un archivo CSV con los biomarcadores", type=["csv"])

if uploaded_file is not None:
    # Leer datos desde el archivo CSV
    data_from_csv = pd.read_csv(uploaded_file)
    
    # Quitar columnas no necesarias
    data_from_csv.drop(columns=['eyesight_left', 'eyesight_right', 'hearing_left', 'hearing_right', 'id'], axis=1, errors='ignore', inplace=True)
    
    # Escalar los datos usando el scaler cargado
    data_from_csv_scaled = scaler.transform(data_from_csv)
    
    # Realizar predicciones
    predictions = mejor_forest.predict(data_from_csv_scaled)
    
    # Crear un DataFrame para mostrar los resultados
    results_df = pd.DataFrame(predictions, columns=['Predicción'])
    results_df.replace({0: 'No Fumador', 1: 'Fumador'}, inplace=True)
    
    # Mostrar los resultados
    st.write("Predicciones basadas en el archivo CSV:")
    st.dataframe(results_df)
else:
    st.write("Por favor, sube un archivo CSV con los datos para realizar predicciones.")

