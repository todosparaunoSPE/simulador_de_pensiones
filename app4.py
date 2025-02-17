# -*- coding: utf-8 -*-
"""
Created on Mon Feb 17 09:27:35 2025

@author: jperezr
"""

import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import os
from pathlib import Path



# Estilo de fondo
page_bg_img = """
<style>
[data-testid="stAppViewContainer"]{
background:
radial-gradient(black 15%, transparent 16%) 0 0,
radial-gradient(black 15%, transparent 16%) 8px 8px,
radial-gradient(rgba(255,255,255,.1) 15%, transparent 20%) 0 1px,
radial-gradient(rgba(255,255,255,.1) 15%, transparent 20%) 8px 9px;
background-color:#282828;
background-size:16px 16px;
</style>
"""

st.markdown(page_bg_img, unsafe_allow_html=True)


def simulate_pension(ahorro_inicial, aportacion_mensual, rendimiento_anual, inflacion_anual, años, estrategia, crisis):
    saldo = ahorro_inicial
    data = []
    total_aportado = ahorro_inicial + (aportacion_mensual * 12 * años)
    for año in range(1, años + 1):
        if estrategia == "Renta fija":
            rendimiento_real = rendimiento_anual - 1  # Menor rendimiento, menor riesgo
        elif estrategia == "Renta variable":
            rendimiento_real = rendimiento_anual + 2  # Mayor rendimiento, mayor riesgo
        else:
            rendimiento_real = rendimiento_anual  # Mixta mantiene el rendimiento base
        
        # Aplicar crisis económica cada 10 años (simulación de crisis)
        if crisis and año % 10 == 0:
            rendimiento_real -= 5  # Reducción del rendimiento temporal
        
        saldo = saldo * (1 + (rendimiento_real - inflacion_anual) / 100) + (aportacion_mensual * 12)
        data.append([año, saldo])
    
    retorno_total = saldo - total_aportado
    return pd.DataFrame(data, columns=["Año", "Saldo Acumulado"]), retorno_total, saldo / (20 * 12)  # Pensión mensual durante 20 años

# Obtener la carpeta de descargas
DOWNLOADS_FOLDER = str(Path.home() / "Downloads")

# Configuración de la aplicación
st.title("Simulador de Pensiones y Estrategias de Inversión")

# Agregar sección de ayuda en el sidebar
st.sidebar.title("Ayuda")
st.sidebar.write("Esta aplicación permite simular el crecimiento de un fondo de pensión con diferentes estrategias de inversión.")
st.sidebar.write("Ingrese los valores de ahorro inicial, aportación mensual, rendimiento e inflación esperados para obtener una proyección a lo largo del tiempo.")

# Entradas del usuario
ahorro_inicial = st.number_input("Ahorro inicial ($):", min_value=0, value=100000, step=10000)
aportacion_mensual = st.number_input("Aportación mensual ($):", min_value=0, value=5000, step=500)
rendimiento_anual = st.slider("Rendimiento anual (%):", 0.0, 15.0, 7.0, 0.1)
inflacion_anual = st.slider("Inflación anual (%):", 0.0, 10.0, 3.0, 0.1)
años = st.slider("Años de inversión:", 1, 40, 30)
estrategia = st.selectbox("Estrategia de inversión:", ["Renta fija", "Renta variable", "Mixta"])
crisis = st.checkbox("Incluir crisis económicas cada 10 años")

# Simulación y visualización
df, retorno_total, pension_mensual = simulate_pension(ahorro_inicial, aportacion_mensual, rendimiento_anual, inflacion_anual, años, estrategia, crisis)
fig = px.line(df, x="Año", y="Saldo Acumulado", title=f"Proyección de Pensión - {estrategia}", markers=True)
st.plotly_chart(fig)

# Mostrar datos
df.index += 1
st.write("### Datos de la Simulación")
st.dataframe(df, use_container_width=True)

# Mostrar resultados clave
st.write(f"**Retorno total:** ${retorno_total:,.2f}")
st.write(f"**Pensión mensual estimada (20 años de retiro):** ${pension_mensual:,.2f}")

# Comparación de estrategias
df_comparacion = pd.DataFrame()
for strat in ["Renta fija", "Renta variable", "Mixta"]:
    df_temp, _, _ = simulate_pension(ahorro_inicial, aportacion_mensual, rendimiento_anual, inflacion_anual, años, strat, crisis)
    df_temp["Estrategia"] = strat
    df_comparacion = pd.concat([df_comparacion, df_temp])
fig_comp = px.line(df_comparacion, x="Año", y="Saldo Acumulado", color="Estrategia", title="Comparación de Estrategias de Inversión")
st.plotly_chart(fig_comp)

# Exportar datos
df.to_csv(os.path.join(DOWNLOADS_FOLDER, "simulacion_pension.csv"), index=False)
df.to_excel(os.path.join(DOWNLOADS_FOLDER, "simulacion_pension.xlsx"), index=False)
st.write("Los datos de la simulación se han guardado en la carpeta de Descargas como CSV y Excel.")

# Agregar información de autor y copyright
st.sidebar.write("**Desarrollado por: Javier Horacio Pérez Ricárdez**")
st.sidebar.write("© 2025 Todos los derechos reservados.")
