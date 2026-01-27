import streamlit as st
import google.generativeai as genai
import os

# Para banners, esta es buena opción:
st.image(
    "https://raw.githubusercontent.com/egyrmexiq-oss/quantum-portal/main/manos_h_y_r.jpg",
    use_container_width=True
)

# Y luego controlas el alto con CSS:
st.markdown(
    """
    <style>
    .stImage > div > img {
        max-height: 125px;
        object-fit: cover;
    }
    </style>
    """,
    unsafe_allow_html=True
)

with st.sidebar:    
# Logo e Identidad
    try:
        st.image("logo_quantum.png", use_container_width=True)
    except:
        st.header("🏋️ Quantum Mind GYM")

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
            Eres el 'Quantum Mind Master'. Usuario: {edad} años. 
            
            PROTOCOLO DE ACCIÓN:
            1. REVISIÓN DE MEMORIA: Mira el historial. 
               - Si el usuario respondió a un reto previo: Evalúa con "¡CORRECTO!" o "INCORRECTO".
               - Si NO hay un reto activo o el usuario está saludando/diciendo "no" o "listo": LANZA DE INMEDIATO un nuevo reto de {disciplina}.
            
            2. EVALUACIÓN ESTRICTA:
               - SI ES INCORRECTO: Da una pista sutil según sus {edad} años. PROHIBIDO cambiar de reto.
               - SI ES CORRECTO: Da el BIO-ANÁLISIS y otorga puntos (1-10) con el código: ##PUNTOS:X##
            
            3. TONO POR EDAD: 
               - 8 años: Detective junior, retos de dulces, juguetes o animales. 
               - Adulto: Arquitecto mental, misterios lógicos profundos.
            """
            
            # Generamos la respuesta
            # --- MEMORIA DINÁMICA ---
            # Tomamos los últimos 4 mensajes para que tenga contexto del reto activo
            historial_reciente = "\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.messages[-4:]])
            
            # Generamos con Memoria + Instrucciones + Mensaje actual
            response = model.generate_content([contexto_gym, historial_reciente, prompt])
            texto_respuesta = response.text
            
            # --- PROCESADOR DE PUNTOS DINÁMICOS ---
            # --- PROCESADOR DE FEEDBACK Y PUNTOS ---
            import re
            match = re.search(r"##PUNTOS:(\d+)##", texto_respuesta)
            
            if match:
                puntos_ganados = int(match.group(1))
                st.session_state.neuro_points += puntos_ganados
                play_sound()
                st.success(f"🌟 ¡RETO SUPERADO! +{puntos_ganados} puntos.")
                st.balloons() 
                texto_respuesta = texto_respuesta.replace(match.group(0), "")
            elif "INCORRECTO" in texto_respuesta.upper():
                # BONO DE PERSEVERANCIA: 1 punto por recibir una pista
                st.session_state.neuro_points += 1
                st.warning("🧠 Sinapsis en proceso... +1 punto de perseverancia. ¡Sigue la pista!")
            
            st.markdown(texto_respuesta)
            st.session_state.messages.append({"role": "assistant", "content": texto_respuesta})
