import pandas as pd
import streamlit as st

def load_data():
    try:
        df = pd.read_excel("data/Datos.xlsx")
        
        # Convertir todos los valores de la columna 'Departamento' a mayúsculas
        if 'Departamento' in df.columns:
            df['Departamento'] = df['Departamento'].str.upper()
        
        return df
    except Exception as e:
        st.error(f"Error al cargar el archivo Datos.xlsx: {str(e)}")
        return None


# src/visualizations/custom_colors.py
CUSTOM_COLORS = {
    'especies': [
        '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd',
        '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf',
        '#aec7e8', '#ffbb78', '#98df8a', '#ff9896', '#c5b0d5'
    ],
    'origen': ['#2ecc71', '#e74c3c', '#3498db', '#f1c40f']
}
