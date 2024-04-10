# Ejecuta este comando en tu terminal para que se abra en local el programa de predicción
# streamlit run src/app/Detector_Fumadores_full.py

import streamlit as st
import pandas as pd
import numpy as np
import joblib
from sklearn.preprocessing import StandardScaler

# Versión para carga de archivos en csv o de forma manual
mejor_forest = joblib.load('src/model/random_forest_model.joblib')
scaler = joblib.load('src/model/scaler.joblib')

st.set_page_config(page_title='Detector de Fumadores', page_icon='🚬', layout='centered', initial_sidebar_state='expanded')
st.title('Detector de Fumadores')
st.write('Esta aplicación predice si una persona es fumadora basada en sus biomarcadores y otras características de salud.')
st.image('src/app/Portada.png', caption='Detector de Fumadores', use_column_width=True)

rangos = {
    "age": (14.0, 120.0),
    "height(cm)": (135.0, 210.0),
    "weight(kg)": (30.0, 150.0),
    "waist(cm)": (51.0, 127.0),
    "eyesight(left)": (0.1, 9.9),
    "eyesight(right)": (0.1, 9.9),
    "hearing(left)": (1.0, 2.0), 
    "hearing(right)": (1.0, 2.0), 
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

categoricas = {
    "dental caries": False
}

method = st.radio("Selecciona el método de entrada de datos", ("Subir archivo CSV", "Introducir datos manualmente"))

if method == "Subir archivo CSV":
    uploaded_file = st.file_uploader("Sube un archivo CSV con los biomarcadores", type=["csv"])

    if uploaded_file is not None:
        data_from_csv = pd.read_csv(uploaded_file)
        print(data_from_csv.columns)
        
        data_from_csv.drop(columns=['eyesight_left', 'eyesight_right', 'hearing_left', 'hearing_right', 'id'], axis=1, errors='ignore', inplace=True)
        columns_order = ['age', 'height(cm)', 'weight(kg)', 'waist(cm)', 'eyesight(left)',
       'eyesight(right)', 'hearing(left)', 'hearing(right)', 'systolic',
       'relaxation', 'fasting blood sugar', 'Cholesterol', 'triglyceride',
       'HDL', 'LDL', 'hemoglobin', 'Urine protein', 'serum creatinine', 'AST',
       'ALT', 'Gtp', 'dental caries']
        data_from_csv = data_from_csv[columns_order]

        data_from_csv_scaled = scaler.transform(data_from_csv)
        
        predictions = mejor_forest.predict(data_from_csv_scaled)
        
        results_df = pd.DataFrame(predictions, columns=['Predicción'])
        results_df.replace({0: 'No Fumador', 1: 'Fumador'}, inplace=True)
        
        st.write("Predicciones basadas en el archivo CSV:")
        st.dataframe(results_df)

if method == "Introducir datos manualmente":
    user_input = {}

    for column, (min_val, max_val) in rangos.items():
        user_input[column] = st.number_input(f"Introduce {column}", min_value=min_val, max_value=max_val, value=(min_val + max_val) / 2)

    dental_caries_input = st.checkbox("Dental caries")
    user_input['dental caries'] = 1 if dental_caries_input else 0

    if st.button('Realizar Predicción'):
        columns_order = ['age', 'height(cm)', 'weight(kg)', 'waist(cm)', 'systolic', 'relaxation', 'fasting blood sugar', 'Cholesterol', 'triglyceride', 'HDL', 'LDL', 'hemoglobin', 'Urine protein', 'serum creatinine', 'AST', 'ALT', 'Gtp', 'dental caries']
        user_data = pd.DataFrame([user_input])[columns_order]

        user_data_scaled = scaler.transform(user_data)

        prediction = mejor_forest.predict(user_data_scaled)

        result = "Fumador" if prediction[0] == 1 else "No Fumador"
        st.write(f"Predicción: {result}")