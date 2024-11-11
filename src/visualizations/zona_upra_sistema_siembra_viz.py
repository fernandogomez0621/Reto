import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from .custom_colors import CUSTOM_COLORS

def show_zona_upra_sistema_siembra_dashboard(df):
    st.header("Distribución por Zona UPRA y Sistema de Siembra")
    
    # Filtrar y ordenar datos por zona UPRA
    zonas_orden = ['CARIBE', 'EJE CAFETERO Y SUR OCCIDENTE', 'ORINOQUÍA', 'OTROS']
    selected_zona = st.selectbox(
        'Seleccione una Zona UPRA',
        zonas_orden,
        key="zona_upra_sistema_selectbox"
    )
    
    # Filtrar datos por zona seleccionada
    df_zona = df[df['Zona UPRA'] == selected_zona]
    
    # Contar frecuencias y calcular porcentajes por sistema de siembra
    sistema_counts = df_zona['Sistema Siembra'].value_counts()
    total_sistema = sistema_counts.sum()
    sistema_pct = (sistema_counts / total_sistema * 100).round(2)
    
    # Preparar datos para visualización
    df_viz = sistema_counts.to_frame(name='count')
    df_viz['percentage'] = sistema_pct
    df_viz = df_viz.sort_values('count', ascending=True)
    
    # Usar los colores personalizados
    colors = CUSTOM_COLORS['siembra'][:len(df_viz)]
    
    # Crear gráfico de barras horizontales
    fig = go.Figure(data=[
        go.Bar(
            y=df_viz.index,
            x=df_viz['count'],
            orientation='h',
            text=[f"{v:,} ({p:.1f}%)" for v, p in zip(df_viz['count'], df_viz['percentage'])],
            textposition='auto',
            marker_color=colors,
            hovertemplate='<b>%{y}</b><br>' +
                         'Cantidad: %{x:,}<br>' +
                         '%{text}<extra></extra>'
        )
    ])
    
    # Configuración del diseño
    fig.update_layout(
        height=max(500, len(df_viz) * 30),  # Altura dinámica
        margin=dict(l=150, r=50, t=70, b=50),
        xaxis_title="Cantidad de Registros",
        yaxis_title="",
        showlegend=False,
        title={
            'text': f"<b>{selected_zona}</b>: Total de registros {total_sistema:,}",
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
    if st.checkbox('Mostrar datos detallados', key=f'show_data_details_{selected_zona}_sistema'):
        st.write("Desglose detallado por sistema de siembra:")
        df_table = df_viz.copy()
        df_table['count'] = df_table['count'].apply(lambda x: f"{x:,}")
        df_table['percentage'] = df_table['percentage'].apply(lambda x: f"{x:.1f}%")
        df_table.columns = ['Cantidad', 'Porcentaje']
        st.dataframe(df_table)