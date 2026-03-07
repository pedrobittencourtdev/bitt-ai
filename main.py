import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

st.set_page_config(
    page_title="Bitt.ai",
    page_icon="🦉",
    layout="centered" # Altere para "wide" se quiser que o chat ocupe a tela toda
)

# --- OCULTANDO ELEMENTOS PADRÃO DO STREAMLIT COM CSS ---
estilo_customizado = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap');

    /* Reset geral */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* Fundo principal */
    .stApp {
        background-color: #0f1117;
    }

    /* Oculta elementos padrão */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Título */
    h1 {
        color: #e8eaf0 !important;
        font-weight: 600 !important;
        letter-spacing: -0.5px;
    }

    /* Caption */
    .stApp p.caption, div[data-testid="stCaptionContainer"] p {
        color: #6b7280 !important;
        font-size: 0.85rem !important;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #161b27 !important;
        border-right: 1px solid #1f2937;
    }
    section[data-testid="stSidebar"] * {
        color: #c9d1e0 !important;
    }

    /* Botões na sidebar */
    section[data-testid="stSidebar"] button {
        background-color: #1f2937 !important;
        border: 1px solid #374151 !important;
        color: #e5e7eb !important;
        border-radius: 8px !important;
        width: 100%;
        transition: background-color 0.2s;
    }
    section[data-testid="stSidebar"] button:hover {
        background-color: #374151 !important;
    }

    /* Balão do usuário */
    div[data-testid="stChatMessage"]:has(div[data-testid="chatAvatarIcon-user"]) {
        background-color: #1a2236 !important;
        border: 1px solid #1f3050 !important;
        border-radius: 12px !important;
        padding: 12px 16px !important;
        margin-bottom: 8px;
    }

    /* Balão do assistente */
    div[data-testid="stChatMessage"]:has(div[data-testid="chatAvatarIcon-assistant"]) {
        background-color: #111827 !important;
        border: 1px solid #1f2937 !important;
        border-radius: 12px !important;
        padding: 12px 16px !important;
        margin-bottom: 8px;
    }

    /* Texto das mensagens */
    div[data-testid="stChatMessage"] p {
        color: #d1d5db !important;
        line-height: 1.65 !important;
        font-size: 0.95rem !important;
    }

    /* Input de chat */
    .stChatInputContainer {
        background-color: #161b27 !important;
        border: 1px solid #374151 !important;
        border-radius: 12px !important;
    }
    .stChatInputContainer textarea {
        color: #e5e7eb !important;
        background-color: transparent !important;
    }
    .stChatInputContainer textarea::placeholder {
        color: #4b5563 !important;
    }

    /* Divisor */
    hr {
        border-color: #1f2937 !important;
    }

    /* Métricas */
    div[data-testid="stMetric"] {
        background-color: #1a2236;
        border: 1px solid #1f2937;
        border-radius: 8px;
        padding: 10px 14px;
    }
    div[data-testid="stMetric"] label {
        color: #6b7280 !important;
        font-size: 0.75rem !important;
    }
    div[data-testid="stMetric"] div {
        color: #e5e7eb !important;
        font-size: 1.1rem !important;
        font-weight: 600 !important;
    }

    /* Download button */
    a[data-testid="stDownloadButton"] button {
        background-color: #1f2937 !important;
        border: 1px solid #374151 !important;
        color: #e5e7eb !important;
        border-radius: 8px !important;
        width: 100%;
    }
</style>
"""
st.markdown(estilo_customizado, unsafe_allow_html=True)

# O comando markdown com unsafe_allow_html=True permite que o CSS funcione
st.markdown(estilo_customizado, unsafe_allow_html=True)

load_dotenv()

#1. Configuração do Gemini (Cole a chave que você pegou no Google AI Studio)
chave_secreta = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=chave_secreta)

modelo_ia = genai.GenerativeModel("gemini-2.5-flash")

with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/4712/4712027.png", width=100) #logo
    st.header("⚙️ Configurações")
    st.write("Bem-vindo ao painel do Bitt.ai.")
    
    # Botão super útil para limpar o histórico
    if st.button("🗑️ Limpar Conversa"):
        st.session_state["lista_mensagens"] = []
        st.rerun() # Atualiza a página imediatamente

# Titulo
st.title("🦉 Bitt.ai")
st.caption("Seu assistente virtual inteligente")

# Cria a lista de mensagens se ela não existir
if not "lista_mensagens" in st.session_state:
    st.session_state["lista_mensagens"] = []

texto_usuario = st.chat_input("Digite a sua mensagem")

# Imprime o histórico na tela toda vez que atualiza
for mensagem in st.session_state["lista_mensagens"]:
    role = mensagem["role"]
    content = mensagem["content"]
    # O Streamlit precisa da palavra "assistant" para colocar o ícone do robô
    icone_streamlit = "assistant" if role == "model" else "user"
    st.chat_message(icone_streamlit).write(content)

if texto_usuario:
    # 1. Mostra a mensagem do usuário e salva no histórico
    st.chat_message("user").write(texto_usuario)
    st.session_state["lista_mensagens"].append({"role": "user", "content": texto_usuario})

    # 2. Converte a sua lista para o formato que o Gemini exige ("parts")
    historico_gemini = []
    for msg in st.session_state["lista_mensagens"]:
        historico_gemini.append({"role": msg["role"], "parts": [msg["content"]]})


    # 3. Chama o Gemini enviando todo o histórico de uma vez
    resposta_ia = modelo_ia.generate_content(historico_gemini)
    texto_resposta_ia = resposta_ia.text

    # 4. Mostra a resposta da IA e salva no histórico

    st.chat_message("assistant").write(texto_resposta_ia)
    st.session_state["lista_mensagens"].append({"role": "model", "content": texto_resposta_ia})



