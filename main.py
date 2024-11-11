import streamlit as st
from PIL import Image
from src.utils.data_loader import load_data
from src.visualizations.especies_viz import show_especies_dashboard
from src.visualizations.origen_viz import show_origen_dashboard
from src.visualizations.departamento_especies_viz import show_departamento_especies_dashboard
from src.visualizations.departamento_origen_viz import show_departamento_origen_dashboard
from src.visualizations.modo_siembra_viz import show_modo_siembra_dashboard
from src.visualizations.departamento_siembra import show_departamento_modo_siembra_dashboard
from src.visualizations.NombreComun_Cientifico import show_nombre_comun_cientifico_table
from src.visualizations.sistema_siembra_viz import show_sistema_siembra_dashboard
from src.visualizations.departamento_siembra_viz import show_departamento_sistema_siembra_dashboard
from src.visualizations.subregion_siembra_viz import show_subregion_modo_siembra_dashboard
from src.visualizations.zona_upra_viz import show_zona_upra_dashboard
from src.visualizations.zona_upra_modo_siembra_viz import show_zona_upra_modo_siembra_dashboard
from src.visualizations.zona_upra_sistema_siembra_viz import show_zona_upra_sistema_siembra_dashboard
from src.visualizations.hectareas_departamento_viz import show_hectareas_departamento_dashboard
from src.visualizations.subregion_hectareas_viz import show_hectareas_subregion_dashboard
from src.visualizations.subregion_forecast_viz import analyze_time_series
from src.visualizations.hectareas_tiempo_viz import show_hectareas_subregion_dashboard_tiempo
from src.visualizations.hectareas_departamento_map import *

# Configurar el título de la página
st.set_page_config(layout="wide", page_title="Dashboard Reforestación")

def main():
    # Crear columnas para mostrar la imagen y el título juntos
    col1, col2 = st.columns([1, 5])

    # Cargar y mostrar la imagen en la primera columna
    image_path = "DatosU.JPG"
    image = Image.open(image_path)
    with col1:
        st.image(image, width=150)  # Ajusta el tamaño según prefieras

    # Colocar el título en la segunda columna
    with col2:
        st.title("Dashboard de Plantación Forestal en Colombia")
        st.markdown("### Agricultura y Desarrollo Rural - Ministerio de Agricultura y Desarrollo Rural")

    # Cargar datos
    df = load_data()
    if df is None:
        return

    # Menú lateral para seleccionar visualización
    option = st.sidebar.selectbox(
        'Seleccione una visualización',
        ["Especies", "Origen", "Especies por Departamento", 
         "Origen por Departamento", "Modo Siembra", 
         "Modo Siembra por Departamento", "Nombre Común y Científico", 
         "Sistema de Siembra", "Sistema Siembra por Departamento",
         "Modo Siembra por Subregión",
         "Zona UPRA",
         "Modo de Siembra por Zona UPRA",
         "Sistema de Siembra por Zona UPRA",
         "Hectareas por Departamento",
         "Hectareas por Subregión",
         "Hectareas acumuladas en el tiempo",
         "Predicción de Hectáreas por Subregión",
         "Mapa de Hectáreas por Departamento"]
    )

    # Ejecutar la visualización correspondiente
    if option == "Especies":
        show_especies_dashboard(df)
    elif option == "Origen":
        show_origen_dashboard(df)
    elif option == "Especies por Departamento":
        show_departamento_especies_dashboard(df)
    elif option == "Origen por Departamento":
        show_departamento_origen_dashboard(df)
    elif option == "Modo Siembra":
        show_modo_siembra_dashboard(df)
    elif option == "Modo Siembra por Departamento":
        show_departamento_modo_siembra_dashboard(df)
    elif option == "Nombre Común y Científico":
        show_nombre_comun_cientifico_table(df)
    elif option == "Sistema de Siembra":
        show_sistema_siembra_dashboard(df)
    elif option == "Sistema Siembra por Departamento":
        show_departamento_sistema_siembra_dashboard(df)
    elif option == "Modo Siembra por Subregión":
        show_subregion_modo_siembra_dashboard(df)
    elif option == "Zona UPRA":
        show_zona_upra_dashboard(df)
    elif option == "Modo de Siembra por Zona UPRA":
        show_zona_upra_modo_siembra_dashboard(df)
    elif option == "Sistema de Siembra por Zona UPRA":
        show_zona_upra_sistema_siembra_dashboard(df)
    elif option == "Hectareas por Departamento":
        show_hectareas_departamento_dashboard(df)
    elif option == "Hectareas por Subregión":
        show_hectareas_subregion_dashboard(df)
    elif option == "Predicción de Hectáreas por Subregión":
        analyze_time_series(df)
    elif option == "Hectareas acumuladas en el tiempo":
        show_hectareas_subregion_dashboard_tiempo(df)

    elif option == "Mapa de Hectáreas por Departamento":
        show_hectareas_departamento_map(df)

    # Colocar autores al final del dashboard
    st.markdown("---")  # Línea divisoria
    st.markdown("**Autores del proyecto:** Karen Barrantes - Universidad Nacional de Colombia, Andres Gomez - Universidad Distrital Francisco Jose de Caldas")

if __name__ == "__main__":
    main()
