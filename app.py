import streamlit as st
import pandas as pd

st.title("⚒️ Mi Herramienta de Geología")

# Entrada de datos técnica
st.subheader("Registro de Muestras")
col1, col2 = st.columns(2)

with col1:
    tipo = st.selectbox("Tipo de Roca", ["Ignea", "Sedimentaria", "Metamórfica"])
with col2:
    ubicacion = st.text_input("Ubicación (Coordenadas)")

if st.button("Registrar Hallazgo"):
    st.success(f"¡Muestra de roca {tipo} registrada en {ubicacion}!")
    st.balloons() # ¡Globos de celebración!