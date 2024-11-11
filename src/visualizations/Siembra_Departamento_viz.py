import streamlit as st
import plotly.graph_objects as go
from .custom_colors import CUSTOM_COLORS

def show_departamento_modo_siembra_dashboard(df):
    st.header("Sistema de Siembra por Departamento")

    # Selector de departamento
    departamentos = sorted(df['Departamento'].unique())
    selected_departamento = st.selectbox('Seleccione un Departamento', departamentos)

    # Filtrar datos por departamento
    df_dept = df[df['Departamento'] == selected_departamento]

    # Calcular conteos de sistemas de siembra
    siembra_counts = df_dept['Sistema Siembra'].value_counts()
    total = siembra_counts.sum()

    # Crear DataFrame combinado con conteos
    df_viz = siembra_counts.to_frame(name='count')
    df_viz = df_viz.sort_values('count', ascending=True)  # Ordenar de menor a mayor

    # Crear figura con Plotly
    fig = go.Figure(data=[
        go.Bar(
            y=df_viz.index,
            x=df_viz['count'],
            orientation='h',
            text=[f'{v:,.0f}' for v in df_viz['count']],
            textposition='auto',
            marker_color=CUSTOM_COLORS['siembra'][:len(df_viz)],
            hovertemplate='%{y}<br>Cantidad: %{x:,}<extra></extra>'
        )
    ])

    # Personalizar diseño
    fig.update_layout(
        height=max(600, len(df_viz) * 30),  # Altura dinámica basada en número de sistemas de siembra
        margin=dict(l=200, r=50, t=50, b=50),
        xaxis_title="Número de registros",
        yaxis_title="",
        showlegend=False,
        title={
            'text': f"{selected_departamento}: Total de registros {total:,}",
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

    # Mostrar tabla de datos
    if st.checkbox('Mostrar datos detallados'):
        st.write("Desglose detallado por sistema de siembra:")
        df_table = df_viz.copy()
        df_table['count'] = df_table['count'].apply(lambda x: f"{x:,.0f}")
        df_table.columns = ['Cantidad']
        st.dataframe(df_table)
