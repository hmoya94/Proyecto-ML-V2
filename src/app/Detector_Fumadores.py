import streamlit as st
import pandas as pd

# Personalización del favicon y la imagen de la app
st.set_page_config(
    page_title='Detector de Fumadores',
    page_icon='🚬',
    layout='centered',
    initial_sidebar_state='expanded'
)

# Título y descripción de la aplicación
st.title('Detector de Fumadores')
st.write('Esta aplicación predice si una persona es fumadora basada en sus biomarcadores y otras características de salud.')

# Cargar y mostrar una imagen (ajusta la ruta de la imagen)
st.image('src/app/Portada.png', caption='Detector de Fumadores', use_column_width=True)

# Definir los rangos para los sliders e inputs
nombre_columnas = {
    "Edad": "age",
    "Altura (cm)": "height(cm)",
    "Peso (kg)": "weight(kg)",
    "Cintura (cm)": "waist(cm)",
    "Visión (ojo izquierdo)": "eyesight(left)",
    "Visión (ojo derecho)": "eyesight(right)",
    "Presión sistólica": "systolic",
    "Relajación": "relaxation",
    "Glucosa en ayunas": "fasting blood sugar",
    "Colesterol": "Cholesterol",
    "Triglicéridos": "triglyceride",
    "HDL": "HDL",
    "LDL": "LDL",
    "Hemoglobina": "hemoglobin",
    "Proteína en orina": "urine protein",
    "Creatinina en suero": "serum creatinine",
    "AST": "AST",
    "ALT": "ALT",
    "GTP": "Gtp",
    "Índice de masa corporal (IMC)": "IMC",
    "Relación altura/cintura": "HW_Ratio",
    "Relación altura/edad": "HA_Ratio",
    "Tiene caries": "dental caries"
}

# Rangos de valores para cada campo
rangos = {
    "Edad": (18, 120),
    "Altura (cm)": (135.0, 210.0),
    "Peso (kg)": (30.0, 150.0),
    "Cintura (cm)": (51.0, 127.0),
    "Visión (ojo izquierdo)": (0.1, 9.9),
    "Visión (ojo derecho)": (0.1, 9.9),
    "Presión sistólica": (77.0, 213.0),
    "Relajación": (44.0, 133.0),
    "Glucosa en ayunas": (46.0, 375.0),
    "Colesterol": (77.0, 393.0),
    "Triglicéridos": (8.0, 766.0),
    "HDL": (9.0, 136.0),
    "LDL": (1.0, 1860.0),
    "Hemoglobina": (4.9, 21.0),
    "Creatinina en suero": (0.1, 9.9),
    "AST": (6.0, 778.0),
    "ALT": (1.0, 2914.0),
    "GTP": (2.0, 999.0),
    "Índice de masa corporal (IMC)": (10.0, 50.0),
    "Relación altura/cintura": (1.0, 4.0),
    "Relación altura/edad": (1.0, 10.0)
}

# Categorías booleanas
categorias = {
    "Tiene caries": False
}

# Subir archivo CSV
uploaded_file = st.file_uploader("Sube un archivo CSV con los biomarcadores", type=["csv"])

# Inicializar variable de datos y flag de prioridad de CSV
data_from_csv = None
use_csv = False

# Si se sube un archivo, cargar los datos y cambiar la prioridad a CSV
if uploaded_file is not None:
    data_from_csv = pd.read_csv(uploaded_file)
    use_csv = st.checkbox('Usar datos del CSV', value=True)

with st.form("Formulario del fumador"):
    st.write("A continuación tienes todos los biomarcadores disponibles para la predicción. No es necesario que rellenes todos los valores, solo de los que dispongas información. Las barras en los laterales están de modo informativo para que puedas ver los rangos de cada biomarcador:")
    
    # Diccionario para almacenar las variables
    variables = {}
    
    # Crear inputs para cada variable numérica
    for display_name,  in nombre_columnas.items():
        min_val, max_val = rangos[]
        
        # Permitir la entrada de datos solo si no estamos usando datos de CSV
        if not use_csv:
            col1, col2 = st.columns(2)
            with col1:
                variables[] = st.number_input(
                    display_name,
                    min_value=min_val, 
                    max_value=max_val, 
                    value=(min_val + max_val) // 2
                )
            
            with col2:
                # Crea una barra deslizable que está desactivada
                st.slider(
                    display_name, 
                    min_value=min_val, 
                    max_value=max_val, 
                    value=variables[],
                    key=f"slider_{}",
                    disabled=True,  # Esto desactiva el slider
                    label_visibility="collapsed"
                )
        else:
            # Mostrar un mensaje si estamos usando datos de CSV
            st.write(f"{display_name}: Los datos se tomarán del CSV.")

    # Añadir desplegables y checkboxes para las categorías booleanas
    for cat, default in categorias.items():
        variables[cat] = st.checkbox(cat, value=default)

    # Botón de envío
    submitted = st.form_submit_button("Enviar")
    if submitted:
        if use_csv:
            # Procesar y mostrar datos de CSV
            st.write("Usando los siguientes valores del CSV:")
            st.dataframe(data_from_csv)
            # Aquí iría la lógica para hacer la predicción usando los datos del CSV
        else:
            st.write("Los valores ingresados manualmente son:")
            st.json(variables)
            # Aquí iría la lógica para hacer la predicción usando los valores manuales

