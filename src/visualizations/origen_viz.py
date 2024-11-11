import streamlit as st
import plotly.graph_objects as go
from ..visualizations.custom_colors import CUSTOM_COLORS

def show_origen_dashboard(df):
    st.header("Distribución por Origen")
   
    # Calcular conteos y porcentajes por origen
    origen_counts = df['Agrupacion por Origen'].value_counts()
    total = origen_counts.sum()
    origen_pct = (origen_counts / total * 100).round(4)
    
    # Ordenar de mayor a menor
    origen_counts = origen_counts.sort_values(ascending=True)
    origen_pct = origen_pct[origen_counts.index]
   
    # Crear figura con Plotly
    fig = go.Figure(data=[
        go.Bar(
            x=origen_counts.values,
            y=origen_counts.index,
            orientation='h',
            text=[f'{count:,} ({pct:.1f}%)' for count, pct in zip(origen_counts.values, origen_pct.values)],
            textposition='auto',
            marker_color=CUSTOM_COLORS['origen'][:len(origen_counts)],
            hovertemplate='%{y}<br>Cantidad: %{x:,}<br>Porcentaje: %{text}<extra></extra>'
        )
    ])
   
    # Personalizar diseño
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
