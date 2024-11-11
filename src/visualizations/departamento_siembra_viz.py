import pandas as pd
import plotly.express as px
import streamlit as st
from .custom_colors import CUSTOM_COLORS

def show_departamento_sistema_siembra_dashboard(df):
    # Ordenar los departamentos alfabéticamente y crear el selector
    departamentos = sorted(df['Departamento'].unique())  # Ordenar solo los departamentos
    selected_departamento = st.selectbox('Seleccione un Departamento', departamentos, key="departamento_siembra")

    # Filtrar el DataFrame para el departamento seleccionado
    df_filtered = df[df['Departamento'] == selected_departamento]

    # Agrupar por sistema de siembra y contar
    df_viz = df_filtered['Sistema Siembra'].value_counts().reset_index()
    df_viz.columns = ['Sistema Siembra', 'Count']
    
    # Calcular el porcentaje
    df_viz['Percentage'] = (df_viz['Count'] / df_viz['Count'].sum()) * 100

    # Crear una columna combinada para mostrar en el gráfico
    df_viz['Text'] = df_viz.apply(lambda row: f"{row['Count']} ({row['Percentage']:.2f}%)", axis=1)

    # Crear el gráfico con Plotly Express y mostrar ambos valores y porcentajes
    fig = px.bar(
        df_viz,
        x='Sistema Siembra',
        y='Count',
        text='Text',  # Mostrar el texto combinado de valor y porcentaje
        color='Sistema Siembra',
        color_discrete_sequence=CUSTOM_COLORS['siembra'][:len(df_viz)],  # Usar colores personalizados
        title=f"Sistema de Siembra en {selected_departamento}"
    )

    # Ajustar el tamaño y el layout del gráfico
    fig.update_traces(textposition='outside')  # Coloca el texto fuera de las barras
    fig.update_layout(
        width=800,  # Ajusta el ancho del gráfico
        height=500,  # Ajusta el alto del gráfico
        xaxis_title="Sistema de Siembra",
        yaxis_title="Cantidad",
        showlegend=False,
        margin=dict(l=40, r=40, t=60, b=40),  # Ajusta márgenes para evitar recortes
        xaxis=dict(showgrid=False),  # Deshabilita la grilla en el eje X
        yaxis=dict(showgrid=False)   # Deshabilita la grilla en el eje Y
    )

    # Mostrar el gráfico en Streamlit
    st.plotly_chart(fig)
