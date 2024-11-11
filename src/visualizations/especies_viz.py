# src/visualizations/especies_viz.py
import streamlit as st
import plotly.graph_objects as go
from ..visualizations.custom_colors import CUSTOM_COLORS

def show_especies_dashboard(df):
    st.header("Distribución por Especies")
    
    # Calcular conteos y porcentajes por especie
    especies_counts = df['Agrupacion por Especies Reforestacion Comercial'].value_counts()
    total = especies_counts.sum()
    especies_pct = (especies_counts / total * 100).round(2)
    
    # Ordenar de mayor a menor
    especies_counts = especies_counts.sort_values(ascending=True)
    especies_pct = especies_pct[especies_counts.index]
    
    # Crear figura con Plotly
    fig = go.Figure(data=[
        go.Bar(
            y=especies_counts.index,
            x=especies_counts.values,
            orientation='h',
            text=[f'{count:,} ({pct:.1f}%)' for count, pct in zip(especies_counts.values, especies_pct.values)],
            textposition='auto',
            marker_color=CUSTOM_COLORS['especies'][:len(especies_counts)],
            hovertemplate='%{y}<br>Cantidad: %{x:,}<br>Porcentaje: %{text}<extra></extra>'
        )
    ])
    
    # Personalizar diseño
    fig.update_layout(
        height=800,
        margin=dict(l=200, r=50, t=50, b=50),
        xaxis_title="Total de registros",
        yaxis_title="",
        showlegend=False,
        title={
            'text': f"Total de registros: {total:,}",
            'y':0.98,
            'x':0.5,
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