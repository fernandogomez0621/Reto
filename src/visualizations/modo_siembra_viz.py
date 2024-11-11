import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from groq import Groq
import os

def get_summary_of_modo_siembra(df):
    """
    Utiliza Groq LLM para generar un resumen de los datos de modos de siembra.
    """
    try:
        # Establecer la API key de Groq
        os.environ['GROQ_API_KEY'] = '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'  
        client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
        
        # Preparar datos para el resumen
        summary_data = df.to_dict()
        
        prompt = f"""Proporciona un resumen sobre la distribución de modos de siembra en Colombia.
        Aquí tienes los datos agregados:
        {summary_data}
        
        Indica:
        1. El modo de siembra más común y su proporción relativa.
        2. El modo de siembra menos común y su proporción relativa.
        3. Observaciones sobre la diversidad de modos de siembra.
        4. Posibles razones para la popularidad de ciertos modos de siembra en Colombia.
        5. Implicaciones de cada modo de siembra en términos de sostenibilidad o eficiencia.
        6. Explica en que consiste cada modo de siembra.

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

def show_modo_siembra_dashboard(df):
    st.header("Modo Siembra")
    
    # Filtrar datos para obtener el conteo de 'Modo Siembra' por categoría
    modo_counts = df['Modo Siembra'].value_counts(ascending=False)
    total_general = modo_counts.sum()
    
    # Crear DataFrame auxiliar para visualización y resumen
    df_viz = modo_counts.to_frame(name='Cantidad')
    df_viz['Porcentaje'] = (df_viz['Cantidad'] / total_general * 100).round(1)
    
    # Lista de colores para cada categoría
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']
    
    # Crear gráfico de barras horizontal para 'Modo Siembra'
    fig = go.Figure()
    
    # Añadir barras para cada categoría de modo siembra en orden descendente
    for i, (modo, count) in enumerate(modo_counts.items()):
        percentage = (count / total_general * 100).round(1)
        fig.add_trace(go.Bar(
            x=[count],
            y=[modo],
            orientation='h',
            text=f"{count:,} ({percentage}%)",
            textposition='auto',
            marker_color=colors[i % len(colors)],
            showlegend=False
        ))
    
    # Añadir el total general como la última barra en la parte inferior
    fig.add_trace(go.Bar(
        x=[total_general],
        y=["Total"],
        orientation='h',
        text=f"{total_general:,} (100%)",
        textposition='auto',
        marker_color='#17becf',
        showlegend=False
    ))

    # Configuración de diseño
    fig.update_layout(
        title="Conteo de Modo Siembra",
        xaxis_title="Recuento de Modo Siembra",
        yaxis_title="Modo Siembra",
        plot_bgcolor="white",
    )
    
    # Mostrar el gráfico en Streamlit
    st.plotly_chart(fig, use_container_width=True)
    
    # Botón para obtener un resumen
    if st.button('Obtener resumen de los modos de siembra'):
        resumen = get_summary_of_modo_siembra(df_viz)
        st.write("**Resumen de los modos de siembra:**")
        st.write(resumen)

    # Mostrar tabla de datos si se selecciona
    if st.checkbox('Mostrar datos detallados'):
        st.write("Desglose detallado por modo de siembra:")
        df_table = df_viz.copy()
        df_table['Cantidad'] = df_table['Cantidad'].apply(lambda x: f"{x:,}")
        df_table['Porcentaje'] = df_table['Porcentaje'].apply(lambda x: f"{x:.1f}%")
        st.dataframe(df_table)
