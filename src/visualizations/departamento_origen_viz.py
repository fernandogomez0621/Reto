import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from ..visualizations.custom_colors import CUSTOM_COLORS

def show_departamento_origen_dashboard(df):
    st.header("Distribución por Origen en cada Departamento")
    
    # Preparar datos
    df_grouped = df.groupby(['Departamento', 'Agrupacion por Origen']).size().reset_index(name='count')
    
    # Calcular totales por departamento para ordenar
    dept_totals = df_grouped.groupby('Departamento')['count'].sum().sort_values(ascending=False)
    
    # Crear figura
    fig = go.Figure()
    
    # Posición inicial para las barras
    y_position = 0
    y_ticks = []
    y_labels = []
    
    # Colores para cada tipo de origen
    origin_colors = {
        'Especie Nativa': '#2ecc71',      # Verde
        'Especie Introducida': '#e74c3c',  # Rojo
        'Otras Nativas': '#3498db',        # Azul
        'n.d.': '#95a5a6'                  # Gris
    }
    
    # Iterar sobre departamentos ordenados por total (mayor a menor)
    for dept in dept_totals.index:
        dept_data = df_grouped[df_grouped['Departamento'] == dept]
        total_dept = dept_totals[dept]
        
        # Agregar barras para cada origen
        x_start = 0
        for _, row in dept_data.iterrows():
            origen = row['Agrupacion por Origen']
            count = row['count']
            percentage = (count / total_dept * 100).round(1)
            
            fig.add_trace(go.Bar(
                x=[count],
                y=[y_position],
                orientation='h',
                name=origen,
                text=f"{count:,} ({percentage}%)",
                textposition='auto',
                marker_color=origin_colors.get(origen, '#95a5a6'),
                showlegend=y_position == 0,  # Mostrar leyenda solo para el primer departamento
                hovertemplate=f"{dept}<br>{origen}<br>Cantidad: %{{x:,}}<br>Porcentaje: {percentage}%<extra></extra>"
            ))
            
            x_start += count
        
        # Guardar posición y etiqueta para el eje Y
        y_ticks.append(y_position)
        y_labels.append(f"{dept} ({total_dept:,})")
        y_position += 1
    
    # Configurar diseño e invertir eje Y para que los departamentos con mayores totales estén arriba
    fig.update_layout(
        barmode='stack',
        height=max(600, len(dept_totals) * 40),
        margin=dict(l=200, r=50, t=50, b=50),
        title={
            'text': "Distribución de Origen por Departamento",
            'y':0.98,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        xaxis_title="Número de registros",
        yaxis=dict(
            ticktext=y_labels,
            tickvals=y_ticks,
            title="",
            autorange="reversed"  # Invertir el orden del eje Y
        ),
        plot_bgcolor='white',
        bargap=0.3,
        xaxis=dict(
            gridcolor='lightgray',
            zerolinecolor='lightgray'
        ),
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Mostrar datos detallados si se solicita, con una clave única
    if st.checkbox('Mostrar datos detallados', key='mostrar_datos_detallados'):
        st.write("Desglose detallado por departamento y origen:")
        df_table = df_grouped.pivot(index='Departamento', 
                                  columns='Agrupacion por Origen', 
                                  values='count').fillna(0)
        df_table = df_table.astype(int)
        df_table['Total'] = df_table.sum(axis=1)
        df_table = df_table.sort_values('Total', ascending=False)
        st.dataframe(df_table)
