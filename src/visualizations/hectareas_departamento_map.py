import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from unidecode import unidecode
import json
from urllib.request import urlopen
from groq import Groq
import os
from ..visualizations.custom_colors import CUSTOM_COLORS

def get_species_summary(df_viz, selected_departamento):
    """
    Utiliza el LLM de Groq para generar un resumen sobre las especies en el departamento seleccionado.
    """
    try:
        os.environ['GROQ_API_KEY'] = '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'
        client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
        
        # Preparar datos para el resumen
        summary_data = df_viz.to_dict()
        
        prompt = f"""Proporciona un resumen sobre las especies de reforestación en el departamento de {selected_departamento}.
        Aquí tienes los datos agregados por especie:
        {summary_data}
        
        Indica:
        1. Las especies con mayor y menor cantidad de hectáreas.
        2. La importancia de cada especie en la región de {selected_departamento}.
        3. Observaciones o patrones notables de reforestación en el departamento.
        
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

def show_hectareas_departamento_map(df):
    st.header("Mapa de Hectáreas por Departamento")

    with urlopen('https://gist.githubusercontent.com/john-guerra/43c7656821069d00dcbc/raw/be6a6e239cd5b5b803c6e7c2ec405b793a9064dd/Colombia.geo.json') as response:
        counties = json.load(response)

    df['Departamento'] = df['Departamento'].str.upper().apply(unidecode)
    df['Departamento'] = df['Departamento'].replace('GUAJIRA', 'LA GUAJIRA')

    resultado = df.groupby('Departamento', as_index=False)['Hectareas (Ha)'].sum()
    resultado.rename(columns={'Hectareas (Ha)': 'Hectareas (Ha)'}, inplace=True)

    fig = go.Figure(go.Choroplethmapbox(
        geojson=counties,
        locations=resultado['Departamento'],
        featureidkey="properties.NOMBRE_DPT",
        z=resultado['Hectareas (Ha)'],
        colorscale='Viridis',
        colorbar_title="Hectáreas (Ha)"
    ))

    fig.update_layout(
        mapbox_style="carto-positron",
        mapbox_zoom=3.4,
        mapbox_center={"lat": 4.570868, "lon": -74.2973328},
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        height=600
    )

    st.plotly_chart(fig, use_container_width=True)

    selected_departamento = st.selectbox("Selecciona un departamento para ver especies", resultado['Departamento'].unique())
    if selected_departamento:
        show_especies_por_departamento(df, selected_departamento)

def show_especies_por_departamento(df, selected_departamento):
    df_dept = df[df['Departamento'] == selected_departamento]
    total_hectareas_dept = df_dept['Hectareas (Ha)'].sum()
    especies_hectareas = df_dept.groupby('Agrupacion por Especies Reforestacion Comercial')['Hectareas (Ha)'].sum()
    df_viz = especies_hectareas.sort_values(ascending=True).to_frame(name='Hectareas (Ha)')

    fig = go.Figure(data=[
        go.Bar(
            y=df_viz.index,
            x=df_viz['Hectareas (Ha)'],
            orientation='h',
            text=[f'{v:,.0f} Ha' for v in df_viz['Hectareas (Ha)']],
            textposition='auto',
            marker_color=CUSTOM_COLORS['especies'][:len(df_viz)],
            hovertemplate='%{y}<br>Hectáreas: %{x:,.0f}<extra></extra>'
        )
    ])

    fig.update_layout(
        height=max(600, len(df_viz) * 30),
        margin=dict(l=200, r=50, t=50, b=50),
        xaxis_title="Hectáreas (Ha)",
        showlegend=False,
        title={
            'text': f"{selected_departamento}: Total de Hectáreas {total_hectareas_dept:,.2f} Ha",
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

    if st.checkbox('Mostrar tabla de especies detallada'):
        df_table = df_viz.copy()
        df_table['Hectareas (Ha)'] = df_table['Hectareas (Ha)'].apply(lambda x: f"{x:,.2f}")
        df_table.columns = ['Hectáreas']
        st.dataframe(df_table)

    if st.button('Obtener resumen de especies'):
        resumen = get_species_summary(df_viz, selected_departamento)
        st.write("**Resumen de las especies en el departamento:**")
        st.write(resumen)
