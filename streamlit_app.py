import streamlit as st
import google.generativeai as genai
import os

def play_sound():
    # Un tono tecnológico corto y elegante
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

# 2. CONEXIÓN (Usa el mismo secreto que ya tienes configurado)
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-2.0-flash-exp')

# 3. BARRA LATERAL - PERFIL DEL ATLETA MENTAL
if "messages" not in st.session_state:
     st.session_state.messages = []
if "neuro_points" not in st.session_state:
    st.session_state.neuro_points = 0
with st.sidebar:
    st.image("logo_quantum.png", use_container_width=True) # Usa tu logo
    st.title("🧠 Mind Gym")
    st.divider()
    
    edad = st.slider("Edad:", 18, 100, 45)
    genero = st.radio("Género:", ["Masculino", "Femenino"], horizontal=True)
    # Sección de Progreso (Debajo de Género)
    st.divider()
    st.metric(label="🧠 Neuro-Agilidad", value=f"{st.session_state.neuro_points} pts")
    
    # Rango dinámico
    rango = "Iniciado Sináptico"
    if st.session_state.neuro_points > 50: rango = "Arquitecto Mental"
    if st.session_state.neuro_points > 100: rango = "Quantum Master"
    
    st.subheader(f"Estatus: {rango}")
    st.divider()
    st.divider()
    disciplina = st.selectbox("Área de Entrenamiento:", [
        "Lógica Deductiva (Misterios)", 
        "Agilidad Verbal (Acertijos)", 
        "Exploración Mental (¿Dónde estoy?)",
        "Atención al Detalle"
    ])
    
    if st.button("🔄 Nuevo Entrenamiento"):
        st.session_state.messages = []
        st.rerun()

# 4. INTERFAZ DE ENTRENAMIENTO
st.title("🏛️ Quantum Mind Gym")
st.caption(f"Entrenando la plasticidad neuronal • Perfil: {genero} de {edad} años")


    
st.session_state.messages = [{"role": "assistant", "content": "Bienvenido al Gym. Selecciona una disciplina y dime: 'Estoy listo para el reto'."}]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. EL GAME MASTER (IA)
if prompt := st.chat_input("Escribe tu respuesta o pide un reto..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
with st.chat_message("user"):
    st.markdown(prompt)

with st.chat_message("assistant"):
with st.spinner("Generando desafío neuronal..."):
            
# El "System Prompt" del Game Master
 # 1. Definimos una base por si acaso (Esto quita el error de Pylance)
# UNIFICADO: El Cerebro del Quantum Mind Master
contexto_gym = f"""
Eres el 'Quantum Mind Master', un arquitecto de la cognición superior. 
USUARIO: {genero}, {edad} años. DISCIPLINA: {disciplina}.

REGLA DE ORO: No generes un reto nuevo hasta que el usuario haya resuelto el actual o pida rendirse. 
Tu prioridad absoluta es EVALUAR la respuesta del usuario.

PROTOCOLO DE RESPUESTA:
1. EVALUACIÓN DE RESPUESTA: Si el usuario intenta resolver el misterio, analiza su lógica con profundidad.
2. SI ACIERTA: 
- Usa obligatoriamente las palabras: "CORRECTO" o "FELICIDADES".
- Felicítalo con autoridad de Arquitecto.
- AÑADE UN 'BIO-ANÁLISIS': Explica qué área cerebral se benefició (ej. Córtex, Hipocampo).
3. SI FALLA: 
- NO des un nuevo reto. Dale una pista "cuántica" (elegante y misteriosa) para estimular su pensamiento lateral.
4. MODOS ESPECIALES:
- Exploración Mental: Actúa como guía ciego. Usa olfato, tacto y sonidos ambientales.
- Lógica: Crea misterios inmersivos y oscuros.
5. NUEVO RETO: Solo si el usuario lo pide o tras haber felicitado un acierto, genera un reto de {disciplina} acorde a sus {edad} años.
"""
         # --- BLOQUE DE RESPUESTA ÚNICO Y UNIFICADO ---
if prompt := st.chat_input("Escribe tu respuesta o pide un reto..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
with st.chat_message("user"):
    st.markdown(prompt)

        # 1. Generamos la respuesta del Master
    response = model.generate_content([contexto_gym, prompt])
    texto_respuesta = response.text

        # 2. Detección Inteligente de Éxito
    palabras_exito = ["felicidades", "correcto", "acertaste", "enhorabuena", "excelente", "logrado"]
    es_exito = any(p in texto_respuesta.lower() for p in palabras_exito)

if es_exito:
    st.session_state.neuro_points += 10
    # Disparador de sonido
    st.markdown('<audio autoplay><source src="https://www.soundjay.com/buttons/sounds/button-37.mp3" type="audio/mpeg"></audio>', unsafe_allow_html=True)
    st.toast("¡Conexión Neuronal Reforzada! +10 pts", icon="🧠")
    st.success("🎯 ¡Reto Superado!") 
else:
    # Mensaje de persistencia si no hay éxito
    st.info("🧬 Sigue procesando... el Master espera tu respuesta definitiva.")

    # 3. Mostrar respuesta del Master y guardar
with st.chat_message("assistant"):
    st.markdown(texto_respuesta)
    st.session_state.messages.append({"role": "assistant", "content": texto_respuesta})
