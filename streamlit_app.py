import streamlit as st
import google.generativeai as genai
import os

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
with st.sidebar:
    st.image("logo_quantum.png", use_container_width=True) # Usa tu logo
    st.title("🧠 Mind Gym")
    st.divider()
    
    edad = st.slider("Edad:", 18, 100, 45)
    genero = st.radio("Género:", ["Masculino", "Femenino"], horizontal=True)
    
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

if "messages" not in st.session_state:
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
            contexto_gym = f"""
            Eres el 'Quantum Mind Master'. Tu misión es evitar la inactividad mental.
            PERFIL: {genero}, {edad} años. DISCIPLINA: {disciplina}.
            
            REGLAS:
            1. Crea retos sofisticados, no infantiles.
            2. Usa la edad del usuario para que el tema sea motivante (referencias culturales o históricas acordes).
            3. Si el usuario falla, dale una pista sutil.
            4. Cuando gane, explica qué proceso cognitivo fortaleció (ej. memoria de trabajo, razonamiento fluido).
            5. Mantén un tono retador, elegante y alentador.
            """
            
            response = model.generate_content([contexto_gym, prompt])
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})