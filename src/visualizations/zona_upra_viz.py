# src/visualizations/zona_upra_viz.py

import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from .custom_colors import CUSTOM_COLORS
from groq import Groq
import os

def show_zona_upra_dashboard(df):
    st.header("Distribución por Zona UPRA")
    
    # Calcular conteos por Zona UPRA
    zona_counts = df['Zona UPRA'].value_counts()
    total = zona_counts.sum()
    
    # Preparar datos para visualización
    df_viz = zona_counts.to_frame(name='count')
    df_viz['percentage'] = (df_viz['count'] / total * 100).round(2)
    df_viz = df_viz.sort_values('count', ascending=True)  # Ordenar de menor a mayor
    
    # Crear gráfico de barras horizontales
    fig = go.Figure(data=[
        go.Bar(
            y=df_viz.index,
            x=df_viz['count'],
            orientation='h',
            text=[f"{v:,} ({p:.1f}%)" for v, p in zip(df_viz['count'], df_viz['percentage'])],
            textposition='auto',
            marker_color=CUSTOM_COLORS['zona_upra'],
            hovertemplate='<b>%{y}</b><br>' +
                         'Cantidad: %{x:,}<br>' +
                         '%{text}<extra></extra>'
        )
    ])
    
    # Configuración del diseño
    fig.update_layout(
        height=400,  # Altura fija ya que son pocas categorías
        margin=dict(l=150, r=50, t=70, b=50),
        xaxis_title="Cantidad de Registros",
        yaxis_title="",
        showlegend=False,
        title={
            'text': f"<b>Total de registros: {total:,}</b>",
            'y': 0.95,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        plot_bgcolor='white',
        bargap=0.2,
        xaxis=dict(
            gridcolor='lightgray',
            zerolinecolor='lightgray',
            tickformat=',d',  # Formato de números con separador de miles
            range=[0, max(df_viz['count']) * 1.1]  # Dar un poco más de espacio para las etiquetas
        ),
        yaxis=dict(
            tickfont=dict(size=12)
        )
    )
    
    # Mostrar gráfico en Streamlit
    st.plotly_chart(fig, use_container_width=True)
    
    # Mostrar tabla de datos si se selecciona
    if st.checkbox('Mostrar datos detallados', key='show_data_details_upra'):
        st.write("Desglose detallado por Zona UPRA:")
        df_table = df_viz.copy()
        df_table['count'] = df_table['count'].apply(lambda x: f"{x:,}")
        df_table['percentage'] = df_table['percentage'].apply(lambda x: f"{x:.1f}%")
        df_table.columns = ['Cantidad', 'Porcentaje']
        st.dataframe(df_table)

    # Funcionalidad para obtener un resumen de las zonas UPRA usando Groq
    if st.button('Mostrar resumen de zonas UPRA'):
        resumen = obtener_resumen_zonas_upra(zona_counts)
        st.write(resumen)

def obtener_resumen_zonas_upra(zona_counts):
    """
    Obtiene un resumen de las zonas UPRA utilizando Groq LLM.
    """
    try:
        os.environ['GROQ_API_KEY'] = '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'
        client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
        
        # Crear un resumen del conteo de zonas
        prompt = "Proporciona un resumen de las zonas UPRA, que son y sus distribuciones: " + ", ".join([f"{zona}: {count}" for zona, count in zona_counts.items()])
        
        chat_completion = client.chat.completions.create(
            model="llama3-groq-70b-8192-tool-use-preview",
            messages=[
                {"role": "system", "content": "Eres un experto en análisis de datos geográficos. Proporciona un resumen útil y conciso."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5,
            max_tokens=500,
            top_p=0.65
        )
        
        return chat_completion.choices[0].message.content
    except Exception as e:
        return f"Error al obtener el resumen: {str(e)}"
