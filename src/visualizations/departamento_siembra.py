import streamlit as st
import plotly.graph_objects as go
import pandas as pd

# Cargar datos
# df = pd.read_csv('tu_archivo.csv') # Cargar tu archivo aquí, si es necesario

def show_departamento_modo_siembra_dashboard(df):
    st.header("Modo de Siembra por Departamento")
    
    # Filtrar y ordenar datos por departamento
    departamentos = sorted(df['Departamento'].unique())
    selected_departamento = st.selectbox('Seleccione un Departamento', departamentos, key="departamento_selectbox")
    
    # Filtrar datos por departamento seleccionado
    df_dept = df[df['Departamento'] == selected_departamento]
    
    # Contar y calcular porcentajes para cada modo de siembra dentro del departamento
    modo_counts = df_dept['Modo Siembra'].value_counts()
    total_modo = modo_counts.sum()
    modo_pct = (modo_counts / total_modo * 100).round(2)
    
    # Preparar datos para visualización
    df_viz = modo_counts.to_frame(name='count')
    df_viz['percentage'] = modo_pct
    df_viz = df_viz.sort_values('count', ascending=True)  # Ordenar de menor a mayor para la visualización
    
    # Colores personalizados para cada categoría de modo de siembra
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b']
    
    # Crear gráfico de barras apiladas
    fig = go.Figure(data=[
        go.Bar(
            y=df_viz.index,
            x=df_viz['count'],
            orientation='h',
            text=[f"{v:,} ({p:.1f}%)" for v, p in zip(df_viz['count'], df_viz['percentage'])],
            textposition='auto',
            marker_color=colors[:len(df_viz)],
            hovertemplate='%{y}<br>Cantidad: %{x:,}<br>%{text}<extra></extra>'
        )
    ])
    
    # Configuración de diseño
    fig.update_layout(
        height=max(600, len(df_viz) * 30),  # Altura dinámica basada en número de categorías
        margin=dict(l=150, r=50, t=50, b=50),
        xaxis_title="Cantidad",
        yaxis_title="Modo de Siembra",
        showlegend=False,
        title={
            'text': f"{selected_departamento}: Total de registros {total_modo:,}",
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
    
    # Mostrar gráfico en Streamlit
    st.plotly_chart(fig, use_container_width=True)
    
    # Mostrar tabla de datos
    if st.checkbox('Mostrar datos detallados', key=f'show_data_details_{selected_departamento}'):
        st.write("Desglose detallado por modo de siembra:")
        df_table = df_viz.copy()
        df_table['count'] = df_table['count'].apply(lambda x: f"{x:,}")
        df_table['percentage'] = df_table['percentage'].apply(lambda x: f"{x:.1f}%")
        df_table.columns = ['Cantidad', 'Porcentaje']
        st.dataframe(df_table)

# Llamar a la función con el DataFrame cargado
# show_departamento_modo_siembra_dashboard(df)
