import streamlit as st
import pandas as pd
from datetime import datetime
import base64
from streamlit_pdf_viewer import pdf_viewer
import time
from pyproj import Transformer



# 1. CONFIGURACIÓN DE LA PÁGINA (Debe ser la primera línea de Streamlit)
st.set_page_config(
    page_title="Geofísica Unida",
    layout="wide",
    initial_sidebar_state="expanded"
)



# 2. BARRA LATERAL (MENÚ DE NAVEGACIÓN)
with st.sidebar:
    st.image("Imagenes/Logos/CIMAT.jpg", caption="CIMAT")
    st.title("Menú Principal")
    
    # El radio button funciona como nuestro selector de páginas
    menu = st.radio(
        "Navega por las secciones:",
        ["Inicio", "Calculadora", "Galería", "Biblioteca"]
    )
    
    st.divider()
    st.info("Desarrollado 100% con Python 🐍")



# --- PÁGINA 1: INICIO ---
if menu == "Inicio":
    st.title("Bienvenido al Portal de Geofísica de la Universidad de El Salvador")
    st.write("Plataforma creada por estudiantes, quienes desean compartir sus conocimientos al mundo.")

    st.divider()
    st.write("A tu izquierda encontrarás el menú de navegación para explorar las distintas secciones de nuestro portal. ¡Disfruta tu visita!")


# --- PÁGINA 2: TOPOGRAFÍA ---
elif menu == "Calculadora":
    st.title("Herramientas Topográficas")
    st.write("Calculos relacionados con la topografía y la geodesia.")
    
    tab1, tab2 = st.tabs(["Calculadora de Pendiente", "Conversor de Coordenadas"])

    with tab1:

        # Fórmula en LaTeX para que se vea profesional
        st.latex(r"Pendiente (\%) = \left( \frac{\text{Cota Mayor} - \text{Cota Menor}}{\text{Distancia Horizontal}} \right) \times 100")
        
        # Formulario para la calculadora
        with st.form("form_pendiente"):
            colA, colB = st.columns(2)
            with colA:
                cota_mayor = st.number_input("Cota Mayor (msnm)", min_value=0.0, value=1200.0)
                cota_menor = st.number_input("Cota Menor (msnm)", min_value=0.0, value=1050.0)
            with colB:
                distancia = st.number_input("Distancia Horizontal en el terreno (metros)", min_value=1.0, value=500.0)
            
            calcular = st.form_submit_button("Calcular Pendiente")
        
        if calcular:
            desnivel = cota_mayor - cota_menor
            pendiente = (desnivel / distancia) * 100
            
            st.success(f" El desnivel es de **{desnivel} metros**.")
            st.warning(f" La pendiente topográfica es del **{pendiente:.2f}%**.")
    with tab2:
        st.write("Conversor de coordenadas geográficas a UTM y viceversa.")
        st.write("Convierte coordenadas entre el sistema Geográfico (WGS84) y UTM.")

        # Creamos dos pestañas para las dos opciones de conversión
        tab1_1, tab2_2 = st.tabs(["Lat/Lon UTM", "UTM Lat/Lon"])

        # --- OPCIÓN 1: GEOGRÁFICAS A UTM ---
        with tab1_1:
            st.write("De Geográficas a UTM")
            col1, col2 = st.columns(2)
            
            with col1:
                # Usamos format="%.6f" para permitir muchos decimales en los grados
                lat = st.number_input("Latitud (Ej: 13.7150):", value=13.7150, format="%.6f")
            with col2:
                lon = st.number_input("Longitud (Ej: -89.2030):", value=-89.2030, format="%.6f")
            
            zona_utm = st.number_input("Zona UTM de destino (Ej: 16):", min_value=1, max_value=60, value=16)
            
            if st.button("Convertir a UTM"):
                # EPSG:4326 es el código mundial para Lat/Lon (WGS84)
                # EPSG:326XX es el código para UTM Norte (donde XX es la zona)
                epsg_origen = "EPSG:4326"
                epsg_destino = f"EPSG:326{zona_utm}" 
                
                # Invocamos la magia de pyproj
                transformador = Transformer.from_crs(epsg_origen, epsg_destino, always_xy=True)
                este, norte = transformador.transform(lon, lat)
                
                st.success("¡Conversión exitosa!")
                col_res1, col_res2 = st.columns(2)
                col_res1.metric("Este (X)", f"{este:.3f} m")
                col_res2.metric("Norte (Y)", f"{norte:.3f} m")

        # --- OPCIÓN 2: UTM A GEOGRÁFICAS ---
        with tab2_2:
            st.write("De UTM a Geográficas")
            col3, col4 = st.columns(2)
            
            with col3:
                este_in = st.number_input("Este / X (m):", value=265000.0, format="%.3f")
            with col4:
                norte_in = st.number_input("Norte / Y (m):", value=1516000.0, format="%.3f")
                
            zona_utm_origen = st.number_input("Zona UTM de origen:", min_value=1, max_value=60, value=16)
            
            if st.button("Convertir a Lat/Lon"):
                epsg_origen_utm = f"EPSG:326{zona_utm_origen}"
                epsg_destino_geo = "EPSG:4326"
                
                transformador_inverso = Transformer.from_crs(epsg_origen_utm, epsg_destino_geo, always_xy=True)
                lon_out, lat_out = transformador_inverso.transform(este_in, norte_in)
                
                st.success("¡Conversión exitosa!")
                col_res3, col_res4 = st.columns(2)
                col_res3.metric("Latitud", f"{lat_out:.6f}°")
                col_res4.metric("Longitud", f"{lon_out:.6f}°")




# --- PÁGINA 3: GALERÍA ---
elif menu == "Galería":
    st.title("Galería de distintos tipos de rocas")
    st.write("Visualización de rocas.")
    
    # Pestañas para dividir el contenido
    tab1, tab2, tab3 = st.tabs(["R. Igneas", "R. Sedimentarias", "R. Metamórficas"])
    
    with tab1:
            st.write("Galería de rocas ígneas de El Salvador.")
            
            # Creamos 3 columnas (puedes cambiar el número a 2, 4, etc.)
            col1, col2, col3, col4, col5, col6, col7 = st.columns(7)
            
            with col1:
                st.image("Imagenes/Rocas/1.png", caption="Gabro")
                
            with col2:
                st.image("Imagenes/Rocas/2.png", caption="Andesita")
                
            with col3:
                st.image("Imagenes/Rocas/3.png", caption="Granito")

            with col4:
                st.image("Imagenes/Rocas/4.png", caption="Diorita")

            with col5:
                st.image("Imagenes/Rocas/5.png", caption="Pumita")

            with col6:
                st.image("Imagenes/Rocas/6.png", caption="Riolita")

            with col7:
                st.image("Imagenes/Rocas/7.png", caption="Ignimbrita")



# --- PÁGINA 4: BIBLIOTECA DIGITAL ---
elif menu == "Biblioteca Digital":
    st.title("Biblioteca Digital")
    st.write("Consulta y descarga nuestros libros rescatados.")

# --- BOTÓN DE DESCARGA ---
    with open("Libros/Tarbuck._ciencias_de_la_tierra.pdf", "rb") as pdf_file:
        PDFbyte = pdf_file.read()

    st.download_button(
        label="Descargar Ciencias de la Tierra - Tarbuck",
        data=PDFbyte,
        file_name="Tarbuck_Ciencias_de_la_Tierra.pdf",
        mime="application/pdf"
    )




