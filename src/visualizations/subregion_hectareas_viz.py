# src/visualizations/subregion_hectareas_viz.py
import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from .custom_colors import CUSTOM_COLORS
from groq import Groq
import os

def get_summary_of_subregion_data(df):
    """
    Utiliza Groq LLM para generar un resumen de los datos de hectáreas por subregión.
    """
    try:
        os.environ['GROQ_API_KEY'] = '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'
        client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
        
        # Preparar datos para el resumen
        summary_data = df.to_dict()
        
        prompt = f"""Proporciona un resumen sobre la distribución de hectáreas por subregión.
        Aquí tienes los datos agregados:
        {summary_data}
        
        Indica:
        1. Subregión con la mayor cantidad de hectáreas.
        2. Subregión con la menor cantidad de hectáreas.
        3. Distribución general en porcentaje.
        4. Observaciones significativas o patrones notables.
        5. Un poco de la importancia de cada Subregión en Colombia.
        
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

def show_hectareas_subregion_dashboard(df):
    st.header("Hectáreas por SubRegión")
    
    # Calcular hectáreas y porcentajes para cada subregión
    hectareas_counts = df.groupby('SubRegión')['Hectareas (Ha)'].sum().round(2)
    total_hectareas = hectareas_counts.sum()
    hectareas_pct = (hectareas_counts / total_hectareas * 100).round(2)
    
    # Preparar datos para visualización
    df_viz = hectareas_counts.to_frame(name='hectareas')
    df_viz['percentage'] = hectareas_pct
    df_viz = df_viz.sort_values('hectareas', ascending=True)
    
    # Usar colores personalizados para las subregiones
    colors = CUSTOM_COLORS['subregion'][:len(df_viz)]
    
    # Crear gráfico de barras horizontales
    fig = go.Figure(data=[
        go.Bar(
            y=df_viz.index,
            x=df_viz['hectareas'],
            orientation='h',
            text=[f"{v:,.0f} ({p:.1f}%)" for v, p in zip(df_viz['hectareas'], df_viz['percentage'])],
            textposition='auto',
            marker=dict(color=colors),
            hovertemplate='<b>%{y}</b><br>' +
                         'Hectáreas: %{x:,.0f}<br>' +
                         '%{text}<extra></extra>'
        )
    ])
    
    # Configuración del diseño
    fig.update_layout(
        height=max(600, len(df_viz) * 30),  # Altura dinámica
        margin=dict(l=150, r=50, t=70, b=50),
        xaxis_title="Hectáreas (Ha)",
        yaxis_title="",
        showlegend=False,
        title={
            'text': f"Total de hectáreas: {total_hectareas:,.0f}",
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
            tickformat=',d'
        ),
        yaxis=dict(
            tickfont=dict(size=12)
        )
    )
    
    # Mostrar gráfico en Streamlit
    st.plotly_chart(fig, use_container_width=True)
    
    # Mostrar tabla de datos si se selecciona
    if st.checkbox('Mostrar datos detallados'):
        st.write("Desglose detallado por subregión:")
        df_table = df_viz.copy()
        df_table['hectareas'] = df_table['hectareas'].apply(lambda x: f"{x:,.2f}")
        df_table['percentage'] = df_table['percentage'].apply(lambda x: f"{x:.1f}%")
        df_table.columns = ['Hectáreas', 'Porcentaje']
        st.dataframe(df_table)
    
    # Botón para obtener un resumen
    if st.button('Obtener resumen de datos'):
        resumen = get_summary_of_subregion_data(df_viz)
        st.write("**Resumen de los datos por subregión:**")
        st.write(resumen)
