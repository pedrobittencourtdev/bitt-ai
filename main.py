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
    /* Oculta o menu de hambúrguer superior */
    #MainMenu {visibility: hidden;}
    
    /* Oculta o rodapé "Made with Streamlit" */
    footer {visibility: hidden;}
    
    /* Oculta o espaço em branco no topo da página */
    header {visibility: hidden;}
    
    /* Exemplo: Mudando a cor do chat input */
    .stChatInputContainer {
        border-radius: 15px;
    }
</style>
"""

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
st.title("✨ Bitt.ai")
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



