import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.tsa.seasonal import seasonal_decompose
from sklearn.metrics import mean_squared_error
import warnings
warnings.filterwarnings('ignore')

def analyze_time_series(df):
    st.header("Predicción de Hectáreas por Año usando Series Temporales")

    # Preparación de datos
    df['Año de Establecimiento'] = pd.to_datetime(df['Año de Establecimiento'], format='%Y', errors='coerce')
    df['Year'] = df['Año de Establecimiento'].dt.year
    df['Hectareas (Ha)'] = pd.to_numeric(df['Hectareas (Ha)'].astype(str).str.replace(',', '.'), errors='coerce')

    # Selector de subregión
    subregiones = df['SubRegión'].unique()
    subregion_seleccionada = st.selectbox("Selecciona una Subregión", sorted(subregiones))

    # Filtrar y preparar datos
    df_subregion = df[df['SubRegión'] == subregion_seleccionada].copy()
    
    # Agregar años faltantes con valor 0
    min_year = df_subregion['Year'].min()
    max_year = df_subregion['Year'].max()
    all_years = pd.DataFrame({'Year': range(min_year, max_year + 1)})
    
    yearly_hectares = df_subregion.groupby('Year')['Hectareas (Ha)'].sum().reset_index()
    yearly_hectares = pd.merge(all_years, yearly_hectares, on='Year', how='left')
    yearly_hectares['Hectareas (Ha)'] = yearly_hectares['Hectareas (Ha)'].fillna(0)
    yearly_hectares = yearly_hectares.sort_values('Year')
    
    # Verificar que hay datos suficientes
    if len(yearly_hectares) < 4:
        st.warning(f"No hay suficientes datos históricos para {subregion_seleccionada}. Se necesitan al menos 4 años de datos.")
        return

    # Crear serie temporal indexada
    ts_data = pd.Series(yearly_hectares['Hectareas (Ha)'].values, 
                       index=pd.DatetimeIndex(yearly_hectares['Year'].astype(str)), 
                       name='Hectareas')

    # Verificar datos nulos o infinitos
    if ts_data.isnull().any() or np.isinf(ts_data).any():
        st.warning("Hay valores nulos o infinitos en los datos. Por favor, revise la calidad de los datos.")
        return

    # Análisis de la serie temporal
    st.subheader("Análisis de la Serie Temporal")
    
    # Descomposición de la serie
    try:
        if len(ts_data) >= 2:
            period = min(len(ts_data)-1, 2)
            decomposition = seasonal_decompose(ts_data, period=period)
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=ts_data.index, y=ts_data.values, name='Original'))
            fig.add_trace(go.Scatter(x=ts_data.index, y=decomposition.trend, name='Tendencia'))
            fig.update_layout(title=f'Serie Original y Tendencia - {subregion_seleccionada}',
                            xaxis_title='Año',
                            yaxis_title='Hectáreas')
            st.plotly_chart(fig)

    except Exception as e:
        st.warning(f"No se pudo realizar la descomposición de la serie: {str(e)}")

    # Modelado y predicción
    try:
        # Calcular la varianza de los datos
        data_variance = np.var(ts_data)
        
        # Si la varianza es muy pequeña, usar un modelo más simple
        if data_variance < 1:
            model = SARIMAX(ts_data,
                          order=(1, 0, 0),
                          seasonal_order=(0, 0, 0, 0))
        else:
            model = SARIMAX(ts_data,
                          order=(1, 1, 1),
                          seasonal_order=(0, 0, 0, 0))

        model_fit = model.fit(disp=False)

        # Realizar predicción
        forecast_steps = 2
        forecast = model_fit.get_forecast(steps=forecast_steps)
        forecast_mean = forecast.predicted_mean
        forecast_ci = forecast.conf_int(alpha=0.32)  # Intervalo de confianza del 68% en lugar del 95%
        
        # Limitar las predicciones basadas en los datos históricos
        max_historical = ts_data.max()
        forecast_mean = np.minimum(forecast_mean, max_historical * 1.5)
        forecast_ci = np.minimum(forecast_ci, max_historical * 2)
        
        # Asegurar predicciones no negativas
        forecast_mean = np.maximum(forecast_mean, 0)
        forecast_ci = np.maximum(forecast_ci, 0)

        # Visualización
        last_year = ts_data.index[-1].year
        future_dates = pd.date_range(start=str(last_year + 1), periods=forecast_steps, freq='Y')
        
        fig = go.Figure()
        
        # Datos históricos
        fig.add_trace(go.Scatter(x=ts_data.index, 
                               y=ts_data.values,
                               name='Datos Históricos',
                               line=dict(color='blue')))
        
        # Predicciones
        fig.add_trace(go.Scatter(x=future_dates, 
                               y=forecast_mean,
                               name='Predicción',
                               line=dict(color='red', dash='dash')))
        
        # Intervalos de confianza
        fig.add_trace(go.Scatter(x=future_dates.tolist() + future_dates.tolist()[::-1],
                               y=forecast_ci.iloc[:, 0].tolist() + forecast_ci.iloc[:, 1].tolist()[::-1],
                               fill='toself',
                               fillcolor='rgba(0,100,80,0.2)',
                               line=dict(color='rgba(255,255,255,0)'),
                               name='Intervalo de Confianza 68%'))
        
        fig.update_layout(title=f'Predicción de Hectáreas para {subregion_seleccionada}',
                         xaxis_title='Año',
                         yaxis_title='Hectáreas')
        
        st.plotly_chart(fig)

        # Mostrar predicciones numéricas
        st.subheader("Predicciones")
        for i, date in enumerate(future_dates):
            st.write(f"Año {date.year}:")
            st.write(f"- Predicción: {forecast_mean[i]:.2f} Ha")
            st.write(f"- Intervalo de confianza: [{forecast_ci.iloc[i, 0]:.2f}, {forecast_ci.iloc[i, 1]:.2f}] Ha")

        # Métricas de error usando datos completos
        predictions = model_fit.get_prediction(start=0)
        y_pred = predictions.predicted_mean
        y_true = ts_data
        mse = mean_squared_error(y_true, y_pred)
        rmse = np.sqrt(mse)
        st.subheader("Métricas del Modelo")
        st.write(f"RMSE (Error cuadrático medio): {rmse:.2f}")

    except Exception as e:
        st.error(f"Error en el modelado: {str(e)}")
        st.write("Sugerencias para mejorar el modelado:")
        st.write("1. Verificar que los datos estén completos y sean consistentes")
        st.write("2. Asegurar que hay suficientes años de datos históricos")
        st.write("3. Revisar valores atípicos o extremos")