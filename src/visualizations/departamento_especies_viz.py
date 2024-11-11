import streamlit as st
import plotly.graph_objects as go
from ..visualizations.custom_colors import CUSTOM_COLORS

def show_departamento_especies_dashboard(df):
    st.header("Especies por Departamento")
    
    # Selector de departamento
    departamentos = sorted(df['Departamento'].unique())
    selected_departamento = st.selectbox('Seleccione un Departamento', departamentos)
    
    # Filtrar datos por departamento
    df_dept = df[df['Departamento'] == selected_departamento]
    
    # Calcular conteos y porcentajes por especie
    especies_counts = df_dept['Agrupacion por Especies Reforestacion Comercial'].value_counts()
    total = especies_counts.sum()
    especies_pct = (especies_counts / total * 100).round(2)
    
    # Crear DataFrame combinado con conteos y porcentajes
    df_viz = especies_counts.to_frame(name='count')
    df_viz['percentage'] = especies_pct
    df_viz = df_viz.sort_values('count', ascending=True)  # Ordenar de menor a mayor
    
    # Crear figura con Plotly
    fig = go.Figure(data=[
        go.Bar(
            y=df_viz.index,
            x=df_viz['count'],
            orientation='h',
            text=[f'{v:,.0f} ({p:.1f}%)' for v, p in zip(df_viz['count'], df_viz['percentage'])],
            textposition='auto',
            marker_color=CUSTOM_COLORS['especies'][:len(df_viz)],
            hovertemplate='%{y}<br>Cantidad: %{x:,}<br>%{text}<extra></extra>'
        )
    ])
    
    # Personalizar diseño
    fig.update_layout(
        height=max(600, len(df_viz) * 30),  # Altura dinámica basada en número de especies
        margin=dict(l=200, r=50, t=50, b=50),
        xaxis_title="Número de registros",
        yaxis_title="",
        showlegend=False,
        title={
            'text': f"{selected_departamento}: Total de registros {total:,}",
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
    
    # Mostrar tabla de datos
    if st.checkbox('Mostrar datos detallados'):
        st.write("Desglose detallado por especie:")
        df_table = df_viz.copy()
        df_table['count'] = df_table['count'].apply(lambda x: f"{x:,.0f}")
        df_table['percentage'] = df_table['percentage'].apply(lambda x: f"{x:.1f}%")
        df_table.columns = ['Cantidad', 'Porcentaje']
        st.dataframe(df_table)