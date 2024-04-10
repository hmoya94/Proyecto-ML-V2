import streamlit as st
import pandas as pd
import numpy as np
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

rangos = {
    "age": (14, 120),
    "height(cm)": (135.0, 210.0),
    "weight(kg)": (30.0, 150.0),
    "waist(cm)": (51.0, 127.0),
    "eyesight(left)": (0.1, 9.9),
    "eyesight(right)": (0.1, 9.9),
    "hearing(left)": (1, 2), 
    "hearing(right)": (1, 2), 
    "systolic": (77.0, 213.0),
    "relaxation": (44.0, 133.0),
    "fasting blood sugar": (46.0, 375.0),
    "Cholesterol": (77.0, 393.0),
    "triglyceride": (8.0, 766.0),
    "HDL": (9.0, 136.0),
    "LDL": (1.0, 1860.0),
    "hemoglobin": (4.9, 21.0),
    "Urine protein": (1.0, 6.0),
    "serum creatinine": (0.1, 9.9),
    "AST": (6.0, 778.0),
    "ALT": (1.0, 2914.0),
    "Gtp": (2.0, 999.0)
}


# Checkbox para las variables categóricas
categoricas = {
    "dental caries": False
}

# Elección del método de entrada
method = st.radio("Selecciona el método de entrada de datos", ("Subir archivo CSV", "Introducir datos manualmente"))

if method == "Subir archivo CSV":
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

elif method == "Introducir datos manualmente":
    # Inicializa un diccionario vacío para los inputs del usuario
    user_input = {}

    # Rellena el diccionario con inputs del usuario para cada columna esperada por el modelo
    for column, (min_val, max_val) in rangos.items():
        # Si es 'dental caries', utiliza un checkbox y convierte el booleano a entero
        if column == "dental caries":
            user_input[column] = int(st.checkbox("Dental caries"))
        else:
            # Usa number_input para las demás variables
            user_input[column] = st.number_input(f"Introduce {column}", min_value=min_val, max_value=max_val, value=(min_val + max_val) / 2)
    
    # Botón para realizar predicción
    if st.button('Realizar Predicción'):
        # Convierte el diccionario de inputs en un DataFrame asegurando el orden de las columnas
        user_data = pd.DataFrame([user_input], columns=rangos.keys())
        
        # Escala los datos del usuario
        user_data_scaled = scaler.transform(user_data)

        # Realiza la predicción
        prediction = mejor_forest.predict(user_data_scaled)

        # Muestra el resultado
        result = "Fumador" if prediction[0] == 1 else "No Fumador"
        st.write(f"Predicción: {result}")


