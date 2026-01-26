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
st.set_page_config(page_title="Quantum Mind Gym", page_icon="🧠", layout="wide")

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
    st.title("🧠 Mind Gym")
    st.divider()
    
    edad = st.slider("Edad:", 18, 100, 45)
    genero = st.radio("Género:", ["Masculino", "Femenino"], horizontal=True)
    
    st.divider()
    st.metric(label="🧠 Neuro-Agilidad", value=f"{st.session_state.neuro_points} pts")
    
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
st.title("🏛️ Quantum Mind Gym")
st.caption(f"Entrenando la plasticidad neuronal • Perfil: {genero} de {edad} años")

# Mostrar historial
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. LÓGICA DEL GAME MASTER
if prompt := st.chat_input("Escribe tu respuesta o pide un reto..."):
    # Guardar y mostrar mensaje del usuario
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generar respuesta de la IA
    with st.chat_message("assistant"):
        with st.spinner("Sincronizando redes neuronales..."):
            contexto_gym = f"""
            Eres el 'Quantum Mind Master'. 
            NIVEL DE DIFICULTAD: Ajusta la complejidad según la edad ({edad} años). 
            - Si la edad es menor a 12 años: Usa retos sencillos, lenguaje lúdico y pistas directas.
            - Si la edad es mayor a 18: Usa retos sofisticados, inmersivos y lenguaje de Arquitecto.

            SISTEMA DE PUNTUACIÓN DINÁMICO:
            - Evalúa la complejidad del reto propuesto (Escala 1 a 10).
            - Si el usuario acierta, otorga el puntaje proporcional. Ej: "¡CORRECTO! Has ganado 4 puntos de Neuro-Agilidad por este reto nivel inicial".
            - IMPORTANTE: Debes decir siempre "CORRECTO" o "FELICIDADES" para activar el contador.

            REGLA DE ORO: No saltes de reto. Sube la dificultad solo cuando el usuario demuestre dominio.
            """
            
            response = model.generate_content([contexto_gym, prompt])
            texto_respuesta = response.text
            
            # Detectar éxito
            palabras_exito = ["felicidades", "correcto", "acertaste", "enhorabuena", "excelente"]
            es_exito = any(p in texto_respuesta.lower() for p in palabras_exito)

            if es_exito:
                st.session_state.neuro_points += 10
                play_sound()
                st.toast("¡Conexión Neuronal Reforzada!", icon="🧠")
                st.success("🎯 ¡Reto Superado!")
            
            st.markdown(texto_respuesta)
            st.session_state.messages.append({"role": "assistant", "content": texto_respuesta})