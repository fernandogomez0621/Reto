import streamlit as st
import plotly.express as px
import pandas as pd

def show_hectareas_subregion_dashboard_tiempo(df):
    st.header("Hectáreas por Subregión a lo largo del tiempo")

    # Convert 'Año de Establecimiento' to datetime, extract the year
    df['Año de Establecimiento'] = pd.to_datetime(df['Año de Establecimiento'], format='%Y', errors='coerce')
    df['Year'] = df['Año de Establecimiento'].dt.year

    # Replace commas with periods in 'Hectareas (Ha)' and convert to numeric
    df['Hectareas (Ha)'] = df['Hectareas (Ha)'].replace({',': '.'}, regex=True).astype(float)

    # Sort and calculate cumulative hectares by subregion and year
    df_sorted = df.sort_values(by=['SubRegión', 'Year'])
    df_sorted['Running_Hectares'] = df_sorted.groupby('SubRegión')['Hectareas (Ha)'].cumsum()

    # Plot the cumulative hectares by subregion over time
    fig = px.line(
        df_sorted,
        x='Year',
        y='Running_Hectares',
        color='SubRegión',
        title="Evolución de Hectáreas por Subregión",
        labels={'Year': 'Año de Establecimiento', 'Running_Hectares': 'Hectáreas Acumuladas'}
    )

    # Update layout for better readability
    fig.update_layout(
        xaxis_title="Año de Establecimiento",
        yaxis_title="Hectáreas Acumuladas",
        plot_bgcolor="white",
    )

    # Display the chart in Streamlit
    st.plotly_chart(fig, use_container_width=True)

# Load your data into a DataFrame (assuming CSV format for simplicity)
# df = pd.read_csv('your_data_file.csv')

# Sample usage in Streamlit app
# show_hectareas_subregion_dashboard(df)
