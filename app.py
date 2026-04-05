import streamlit as st
import pandas as pd
from datetime import datetime

# 1. CONFIGURACIÓN DE LA PÁGINA (Debe ser la primera línea de Streamlit)
st.set_page_config(
    page_title="Geofísica Unida",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. SISTEMA DE MEMORIA (Session State para guardar los comentarios)
if "comentarios" not in st.session_state:
    st.session_state.comentarios = []

# 3. BARRA LATERAL (MENÚ DE NAVEGACIÓN)
with st.sidebar:
    st.image("Imagenes/Logos/CIMAT.jpg", caption="CIMAT")
    st.title("Menú Principal")
    
    # El radio button funciona como nuestro selector de páginas
    menu = st.radio(
        "Navega por las secciones:",
        ["Inicio", "Calculadora Topográfica", "Galería de Campo", "Foro de Discusión"]
    )
    
    st.divider()
    st.info("Desarrollado 100% con Python 🐍")

# ==========================================
# 4. LÓGICA DE LAS PÁGINAS (Según lo elegido en el menú)
# ==========================================

# --- PÁGINA 1: INICIO ---
if menu == "Inicio":
    st.title("Bienvenido al Portal de Geofísica de la Universidad de El Salvador")
    st.write("Plataforma creada por estudiantes, quienes desean compartir sus conocimientos al mundo.")
    
    # Columnas para organizar la información
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Objetivos del Proyecto")
        st.write("""
        *  **Topografía:** Cálculo de variables útiles para un geofísico o geólogo.
        *  **Base de datos:** Recopilación de datos en campo.
        """)
    with col2:
        st.info("**Dato curioso:** ¿Sabías que El Salvador está en el Cinturón de Fuego del Pacífico? La actividad volcánica y tectónica hace " \
        "que la geofísica sea una disciplina vital para el país.")

# --- PÁGINA 2: TOPOGRAFÍA ---
elif menu == "Calculadora Topográfica":
    st.title("Herramientas Topográficas")
    st.write("Calcula la pendiente entre dos puntos de un mapa físico (ej. escala 1:25,000).")
    
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

# --- PÁGINA 3: GALERÍA ---
elif menu == "Galería de Campo":
    st.title("Galería de distintos tipos de rocas")
    st.write("Visualización de ejemplos de campo.")
    
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

# --- PÁGINA 4: FORO ---
elif menu == "Foro de Discusión":
    st.title("Foro y Comentarios")
    st.write("Deja tu reporte de campo o comenta sobre la página. (Los comentarios se guardan en la memoria temporal de tu sesión).")
    
    # Cajón de entrada para el usuario
    with st.container():
        nombre = st.text_input("Tu Nombre / Código de Estudiante")
        mensaje = st.text_area("Escribe tu reporte o mensaje aquí...")
        
        if st.button("Enviar Comentario"):
            if nombre and mensaje:
                # Guardamos la fecha y hora actual
                hora_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                # Agregamos el comentario a la lista en la "memoria"
                st.session_state.comentarios.append({
                    "nombre": nombre,
                    "mensaje": mensaje,
                    "fecha": hora_actual
                })
                st.success("¡Comentario publicado!")
            else:
                st.error("Por favor, llena tu nombre y el mensaje.")
    
    st.divider()
    st.subheader("Bandeja de Mensajes y Reportes")
    
    # Mostrar todos los comentarios guardados
    if len(st.session_state.comentarios) == 0:
        st.info("Aún no hay comentarios. ¡Sé el primero en escribir!")
    else:
        # Invertimos la lista para que el más nuevo salga arriba
        for c in reversed(st.session_state.comentarios):
            with st.chat_message("user"):
                st.markdown(f"**{c['nombre']}** - *{c['fecha']}*")
                st.write(c['mensaje'])