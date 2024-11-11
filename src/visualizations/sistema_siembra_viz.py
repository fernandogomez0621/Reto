# src/visualizations/sistema_siembra_viz.py

import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from .custom_colors import CUSTOM_COLORS
from groq import Groq
import os

def get_summary_of_sistema_siembra(df):
    """
    Utiliza Groq LLM para generar un resumen de los datos de sistemas de siembra.
    """
    try:
        # Establecer la API key de Groq
        os.environ['GROQ_API_KEY'] = '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'  
        client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
        
        # Preparar datos para el resumen
        summary_data = df.to_dict()
        
        prompt = f"""Proporciona un resumen sobre la distribución de sistemas de siembra en Colombia.
        Aquí tienes los datos agregados:
        {summary_data}
        
        Indica:
        1. El sistema de siembra más común y su proporción relativa.
        2. El sistema de siembra menos común y su proporción relativa.
        3. Observaciones sobre la diversidad de sistemas de siembra utilizados.
        4. Posibles razones para la popularidad de ciertos sistemas de siembra en Colombia.
        5. Implicaciones en la sostenibilidad o eficiencia agrícola de los diferentes modos de siembra.
        6. Explica brevemente en que consiste cada sistema de siembra.
        Proporciona la información de forma breve y clara."""

        chat_completion = client.chat.completions.create(
            model="llama3-groq-70b-8192-tool-use-preview",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5,
            max_tokens=500,
            top_p=0.65
        )
        
        return chat_completion.choices[0].message.content
    except Exception as e:
        return f"Error al obtener el resumen: {str(e)}"

def show_sistema_siembra_dashboard(df):
    st.header("Distribución por Sistema Siembra")
   
    # Calcular conteos y porcentajes por sistema de siembra
    siembra_counts = df['Sistema Siembra'].value_counts(ascending=True)
    total = siembra_counts.sum()
    siembra_pct = (siembra_counts / total * 100).round(4)
    
    # Crear DataFrame auxiliar para visualización y resumen
    df_viz = siembra_counts.to_frame(name='Cantidad')
    df_viz['Porcentaje'] = siembra_pct
    df_viz = df_viz.sort_values('Cantidad', ascending=True)
    
    # Crear gráfico de barras horizontales
    fig = go.Figure(data=[
        go.Bar(
            x=df_viz['Cantidad'].values,
            y=df_viz.index,
            orientation='h',
            text=[f"{count:,} ({pct:.1f}%)" for count, pct in zip(df_viz['Cantidad'], df_viz['Porcentaje'])],
            textposition='auto',
            marker_color=CUSTOM_COLORS['modo_siembra'][:len(df_viz)],
            hovertemplate='%{y}<br>Cantidad: %{x:,}<br>Porcentaje: %{text}<extra></extra>'
        )
    ])
   
    # Personalizar diseño del gráfico
    fig.update_layout(
        height=400,
        margin=dict(l=200, r=50, t=50, b=50),
        xaxis_title="Número de registros",
        yaxis_title="",
        showlegend=False,
        title={
            'text': f"Total de registros: {total:,}",
            'y': 0.98,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        plot_bgcolor='white',
        bargap=0.2,
        xaxis=dict(
            gridcolor='lightgray',
            zerolinecolor='lightgray'
        )
    )
   
    st.plotly_chart(fig, use_container_width=True)
    
    # Botón para obtener un resumen
    if st.button('Obtener resumen de los modos de siembra'):
        resumen = get_summary_of_sistema_siembra(df_viz)
        st.write("**Resumen de los sistemas de siembra:**")
        st.write(resumen)

    # Mostrar tabla de datos si se selecciona
    if st.checkbox('Mostrar datos detallados'):
        st.write("Desglose detallado por sistema de siembra:")
        df_table = df_viz.copy()
        df_table['Cantidad'] = df_table['Cantidad'].apply(lambda x: f"{x:,}")
        df_table['Porcentaje'] = df_table['Porcentaje'].apply(lambda x: f"{x:.2f}%")
        st.dataframe(df_table)
