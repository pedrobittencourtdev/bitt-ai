import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

st.set_page_config(
    page_title="Bitt.ai",
    page_icon="🦉",
    layout="centered"
)

# --- OCULTANDO ELEMENTOS PADRÃO DO STREAMLIT COM CSS ---
estilo_customizado = """
<style>
    /* Oculta o menu de hambúrguer superior */
    #MainMenu {visibility: hidden;}
    
    /* Oculta o rodapé "Made with Streamlit" */
    footer {visibility: hidden;}
    
    /* Exemplo: Mudando a cor do chat input */
    .stChatInputContainer {
        border-radius: 15px;
    }
</style>
"""

# O comando markdown com unsafe_allow_html=True permite que o CSS funcione
st.markdown(estilo_customizado, unsafe_allow_html=True)

load_dotenv()

# 1. Configuração do Gemini (Cole a chave que você pegou no Google AI Studio)
chave_secreta = os.getenv("GEMINI_API_KEY")
if chave_secreta:
    api_configurada = True
    genai.configure(api_key=chave_secreta)
    modelo_ia = genai.GenerativeModel("gemini-2.5-flash")
else:
    api_configurada = False
    
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/4712/4712027.png", width=100) #logo
    st.header("⚙️ Configurações")
    st.write("Bem-vindo ao painel do Bitt.ai.")
    
    # Botão super útil para limpar o histórico
    if st.button("🗑️ Limpar Conversa"):
        st.session_state["lista_mensagens"] = []
        st.rerun() # Atualiza a página imediatamente

    st.divider() # Cria uma linha separadora bem sutil
    st.markdown("<div style='text-align: center;'><small>Desenvolvido por <a href='https://github.com/pedrobittencourtdev' target='_blank' style='color: #00E676; text-decoration: none;'>Pedro Bittencourt</a></small></div>", unsafe_allow_html=True)

# Titulo
st.title("🦉 Bitt.ai")
st.caption("Assistente Corporativo · Profissional · Preciso")

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
    # 1. Verifica se a API está configurada ANTES de fazer qualquer coisa
    if not api_configurada:
        st.error("❌ Não é possível enviar mensagens sem uma chave de API válida.")
    else:
        # 2. Mostra a mensagem do usuário e salva no histórico
        st.chat_message("user").write(texto_usuario)
        st.session_state["lista_mensagens"].append({"role": "user", "content": texto_usuario})

        # 3. Converte a sua lista para o formato que o Gemini exige ("parts")
        historico_gemini = []
        for msg in st.session_state["lista_mensagens"]:
            historico_gemini.append({"role": msg["role"], "parts": [msg["content"]]})

        # 4. Chama o Gemini com Streaming e Spinner
        with st.chat_message("assistant"):
            with st.spinner("Processando..."):
                try:
                    resposta_stream = modelo_ia.generate_content(
                        historico_gemini,
                        stream=True
                    )

                    # Cria um pequeno "motor" para entregar as palavras uma a uma
                    def gerador_de_texto():
                        for chunk in resposta_stream:
                            if chunk.text:
                                yield chunk.text

                    # A função mágica do Streamlit: faz a animação sozinha e já guarda o texto inteiro
                    texto_completo = st.write_stream(gerador_de_texto())

                    # 5. Salva a resposta da IA no histórico!
                    st.session_state["lista_mensagens"].append({"role": "model", "content": texto_completo})

                except genai.types.generation_types.BlockedPromptException:
                    st.warning("⚠️ Esta mensagem foi bloqueada pelas políticas de segurança da API.")
                except Exception as e:
                    st.error(f"❌ **Erro ao processar a resposta:** {e}")