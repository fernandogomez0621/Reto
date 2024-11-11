import streamlit as st
import pandas as pd
from groq import Groq
import os

def get_plant_info(nombre_planta, nombre_cientifico=None):
    """
    Obtiene información detallada de una planta específica usando Groq LLM.
    """
    try:
        os.environ['GROQ_API_KEY'] = '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'
        client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
        
        prompt = f"""Por favor proporciona información detallada sobre la siguiente planta:
        Nombre común: {nombre_planta}
        {f'Nombre científico: {nombre_cientifico}' if nombre_cientifico else ''}
        
        Incluye los siguientes aspectos:
        1. Descripción general
        2. Hábitat natural
        3. Características de cultivo
        4. Usos comerciales
        5. Beneficios ambientales
        
        Formatea la respuesta de manera clara y concisa."""

        chat_completion = client.chat.completions.create(
            model="llama3-groq-70b-8192-tool-use-preview",
            messages=[
                {"role": "system", "content": "Eres un experto botánico. Proporciona información precisa y útil sobre plantas."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5,
            max_tokens=1000,
            top_p=0.65
        )
        
        return chat_completion.choices[0].message.content
    except Exception as e:
        return f"Error al obtener información: {str(e)}"

def show_nombre_comun_cientifico_table(df):
    # Crear un espacio antes del encabezado principal
    st.markdown("<br>", unsafe_allow_html=True)
    st.header("Tabla de Nombres Comunes y Científicos")
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Crear una copia del DataFrame y procesar valores nulos y "n.d"
    df_copia = df[['Nombre Comun', 'Nombre Cientifico']].copy()
    
    # Reemplazar 'n.d.' y otros valores por 'No Disponible'
    df_copia['Nombre Comun'] = df_copia['Nombre Comun'].replace(['', 'n.d.', None], 'No Disponible')
    df_copia['Nombre Cientifico'] = df_copia['Nombre Cientifico'].replace(['', 'n.d.', None], 'No Disponible')
    
    # Eliminar filas donde ambos valores sean 'No Disponible'
    df_copia = df_copia[~((df_copia['Nombre Comun'] == 'No Disponible') & 
                          (df_copia['Nombre Cientifico'] == 'No Disponible'))]
    
    # Eliminar filas duplicadas y ordenar por nombre común
    nombres_unicos = df_copia.drop_duplicates(subset=['Nombre Comun', 'Nombre Cientifico']).sort_values('Nombre Comun')
    
    # Crear columnas para dividir la pantalla
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Mostrar la tabla utilizando `st.table`, sin índice
        st.table(nombres_unicos.reset_index(drop=True))  # Restablecer índice y no mostrar

        # Agregar opción para ver datos adicionales
        if st.checkbox('Mostrar datos adicionales', key='mostrar_especies_datos'):
            st.markdown("<br>", unsafe_allow_html=True)
            st.write("Resumen de especies (basado en Nombre Común):")
            total_especies = len(nombres_unicos)
            especies_con_comun = nombres_unicos['Nombre Comun'].apply(
                lambda x: x != 'No Disponible'
            ).sum()
            especies_sin_comun = total_especies - especies_con_comun
            
            col_a, col_b, col_c = st.columns(3)
            col_a.metric("Total de Especies", f"{total_especies:,}")
            col_b.metric("Con Nombre Común", f"{especies_con_comun:,}")
            col_c.metric("Sin Nombre Común", f"{especies_sin_comun:,}")
    
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        st.subheader("Información Detallada de Especies")
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Selector de planta (usando los nombres originales para la selección)
        planta_seleccionada = st.selectbox(
            "Seleccione una especie:",
            options=nombres_unicos['Nombre Comun'].unique(),
            key='planta_selector'
        )
        
        if planta_seleccionada:
            # Obtener el nombre científico correspondiente
            nombre_cientifico = nombres_unicos[
                nombres_unicos['Nombre Comun'] == planta_seleccionada
            ]['Nombre Cientifico'].iloc[0]
            
            st.markdown(f"**Nombre común:** {planta_seleccionada}")
            if nombre_cientifico != 'No Disponible':
                st.markdown(f"**Nombre científico:** *{nombre_cientifico}*")
            else:
                st.markdown("**Nombre científico:** *No Disponible*")
            
            # Botón para obtener información detallada
            if st.button("Obtener información detallada", key='get_info_button'):
                with st.spinner("Consultando información..."):
                    info = get_plant_info(
                        planta_seleccionada, 
                        nombre_cientifico if nombre_cientifico != 'No Disponible' else None
                    )
                    st.markdown("### Información")
                    st.markdown(info)

# Cargar los datos en el DataFrame
# df = pd.read_csv('ruta_a_tu_archivo.csv')
# show_nombre_comun_cientifico_table(df)
