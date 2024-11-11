import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from ..visualizations.custom_colors import CUSTOM_COLORS

def show_hectareas_departamento_dashboard(df):
    st.header("Hectáreas por Departamento")
   
    # Calcular hectáreas y porcentajes por departamento
    hectareas_dep = df.groupby('Departamento')['Hectareas (Ha)'].sum().round(2)
    total = hectareas_dep.sum()
    hectareas_pct = (hectareas_dep / total * 100).round(2)
   
    # Ordenar de menor a mayor
    hectareas_dep = hectareas_dep.sort_values(ascending=True)
    hectareas_pct = hectareas_pct[hectareas_dep.index]
   
    # Calcular el valor máximo para el rango del eje X
    max_value = hectareas_dep.max()
   
    # Crear las listas para el texto y su posición
    text_list = []
    for value, pct in zip(hectareas_dep.values, hectareas_pct.values):
        text = f'{value:,.0f} ({pct:.1f}%)'
        text_list.append(text)

    # Definir colores para cada departamento (reutilizando colores si es necesario)
    color_list = CUSTOM_COLORS['departamentos'] * (len(hectareas_dep) // len(CUSTOM_COLORS['departamentos']) + 1)
   
    # Crear figura con Plotly
    fig = go.Figure(data=[
        go.Bar(
            y=hectareas_dep.index,
            x=hectareas_dep.values,
            orientation='h',
            text=text_list,
            textposition='outside',  # Todo el texto fuera de las barras
            marker_color=color_list[:len(hectareas_dep)],  # Asigna los colores
            hovertemplate='%{y}<br>Hectáreas: %{x:,.0f}<br>Porcentaje: %{text}<extra></extra>'
        )
    ])
   
    # Personalizar diseño
    fig.update_layout(
        height=1200,
        margin=dict(l=200, r=250, t=50, b=50),  # Aumentado el margen derecho para el texto
        xaxis_title="Hectáreas (Ha)",
        yaxis_title="",
        showlegend=False,
        title={
            'text': f"Total de hectáreas: {total:,.0f}",
            'y':0.98,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        plot_bgcolor='white',
        bargap=0.3,
        xaxis=dict(
            gridcolor='lightgray',
            zerolinecolor='lightgray',
            showgrid=True,
            tickformat=',d',
            range=[0, max_value * 1.4]  # Aumentado para dar más espacio al texto externo
        ),
        yaxis=dict(
            tickfont=dict(size=13),
            tickmode='linear',
            automargin=True
        ),
        font=dict(
            size=13
        )
    )
   
    # Ajustar ancho de las barras y formato del texto
    fig.update_traces(
        width=0.6,
        textfont=dict(
            size=13,
            color='black'  # Todo el texto en negro
        ),
        textangle=0,
        cliponaxis=False
    )
   
    st.plotly_chart(fig, use_container_width=True)
   
    # Mostrar datos detallados
    if st.checkbox('Mostrar datos detallados', key='show_data_details_hectareas_dep'):
        st.write("Desglose detallado:")
        df_table = pd.DataFrame({
            'Hectáreas': [f"{v:,.2f}" for v in hectareas_dep.values],
            'Porcentaje': [f"{p:.1f}%" for p in hectareas_pct.values]
        }, index=hectareas_dep.index)
        st.dataframe(df_table)
