import streamlit as st
import google.generativeai as genai
import os

def play_sound():
    sound_html = """
    <audio autoplay>
    <source src="https://www.soundjay.com/buttons/sounds/button-37.mp3" type="audio/mpeg">
    </audio>
    """
    st.markdown(sound_html, unsafe_allow_html=True)

# 1. CONFIGURACIÓN Y ESTILO MIND
st.set_page_config(page_title="Quantum Mind Gym", page_icon="🏋️", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #050510; }
    [data-testid="stSidebar"] { background-color: #0a0a20; border-right: 1px solid #4b0082; }
    div.stButton > button:first-child { 
        background-color: #7b2cbf; color: white; border: none; 
        box-shadow: 0 0 10px #7b2cbf; font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. CONEXIÓN Y ESTADO
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-2.0-flash-exp')

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Bienvenido al Gym. Selecciona una disciplina y dime: 'Estoy listo para el reto'."}]
if "neuro_points" not in st.session_state:
    st.session_state.neuro_points = 0

# 3. BARRA LATERAL
with st.sidebar:
    st.title("🏋️ Mind Gym")
    st.divider()
    
    edad = st.slider("Edad:", 8, 100, 45)
    genero = st.radio("Género:", ["Masculino", "Femenino"], horizontal=True)
    
    st.divider()
    st.metric(label="🏋️ Neuro-Agilidad", value=f"{st.session_state.neuro_points} pts")
    
    rango = "Iniciado Sináptico"
    if st.session_state.neuro_points > 50: rango = "Arquitecto Mental"
    if st.session_state.neuro_points > 100: rango = "Quantum Master"
    st.subheader(f"Estatus: {rango}")
    st.divider()

    disciplina = st.selectbox("Área de Entrenamiento:", [
        "Lógica Deductiva (Misterios)", 
        "Agilidad Verbal (Acertijos)", 
        "Exploración Mental (¿Dónde estoy?)",
        "Atención al Detalle"
    ])
    
    if st.button("🔄 Nuevo Entrenamiento"):
        st.session_state.messages = [{"role": "assistant", "content": "Sesión reiniciada. ¿Listo para el siguiente nivel?"}]
        st.rerun()

# 4. INTERFAZ PRINCIPAL
# 4. INTERFAZ PRINCIPAL
st.title("🏛️ Quantum Mind Gym")
st.caption(f"Entrenando la plasticidad neuronal • Perfil: {genero} de {edad} años")

# Mostrar historial de mensajes
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. LÓGICA DEL GAME MASTER CON PUNTUACIÓN DINÁMICA
# 5. LÓGICA DEL GAME MASTER CON PUNTUACIÓN DINÁMICA
if prompt := st.chat_input("Escribe tu pregunta, o tu respuesta o pide un reto..."):
    # Guardamos y mostramos el mensaje del usuario
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Sincronizando redes neuronales..."):
            # El Master ahora lee la EDAD real del slider
            contexto_gym = f"""
            Eres el 'Quantum Mind Master'. 
            NIVEL DE DIFICULTAD: Ajusta la complejidad estrictamente a la edad: {edad} años.
            - Si tiene entre 8 y 12 años: Usa retos muy simples (colores, animales, lógica básica), lenguaje divertido y tono de "superpoderes".
            - Si es adulto: Usa retos crípticos, misterios oscuros y lenguaje técnico de Arquitecto Mental.

            SISTEMA DE PUNTUACIÓN (1-10):
            - Evalúa la dificultad del reto que propusiste.
            - Si el usuario acierta, asigna un puntaje de 1 a 10.
            - OBLIGATORIO: Si acierta, incluye al final de tu respuesta: ##PUNTOS:X## (donde X es el puntaje).
            
            PROTOCOLO:
            1. EVALUAR: Si acierta, di "CORRECTO", da el BIO-ANÁLISIS y el código de puntos.
            2. PERSISTENCIA: No cambies de reto hasta que lo resuelva o se rinda.
            """
            
            # Generamos la respuesta
            response = model.generate_content([contexto_gym, prompt])
            texto_respuesta = response.text
            
            # --- PROCESADOR DE PUNTOS DINÁMICOS ---
            import re
            match = re.search(r"##PUNTOS:(\d+)##", texto_respuesta)
            
            if match:
                puntos_ganados = int(match.group(1))
                st.session_state.neuro_points += puntos_ganados
                # Disparamos el sonido de éxito
                st.markdown('<audio autoplay><source src="https://www.soundjay.com/buttons/sounds/button-37.mp3" type="audio/mpeg"></audio>', unsafe_allow_html=True)
                st.toast(f"¡Neuro-Agilidad +{puntos_ganados} pts!", icon="🏋️")
                st.success(f"🎯 ¡Reto Superado! Ganaste {puntos_ganados} puntos.")
                # Limpiamos el código técnico del mensaje para que el usuario no lo vea
                texto_respuesta = texto_respuesta.replace(match.group(0), "")
            
            # Mostramos la respuesta final y guardamos
            st.markdown(texto_respuesta)
            st.session_state.messages.append({"role": "assistant", "content": texto_respuesta})