import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
import PyPDF2

st.set_page_config(
    page_title="Bitt.ai",
    page_icon="🦉",
    layout="centered"
)

# --- OCULTANDO ELEMENTOS PADRÃO DO STREAMLIT COM CSS ---

# --- CSS RESPONSIVO PARA MOBILE (ANDROID/IOS) ---
estilo_customizado = """
<style>
    /* 1. Limpeza Geral de Elementos do Streamlit */
    #MainMenu {display: none !important;}
    .stDeployButton {display: none !important;}
    footer {display: none !important;}
    .viewerBadge-container {display: none !important;}
    header {background-color: transparent !important;}

    /* 2. Ajuste de Espaçamento no Topo (Mobile) */
    .main .block-container {
        padding-top: 2rem !important;
        padding-bottom: 5rem !important;
    }

    /* 3. Estilização da Caixa de Chat (Arredondada e Centralizada) */
    .stChatInputContainer {
        border-radius: 20px !important;
        bottom: 20px !important; /* Levanta um pouco a barra no iOS */
    }
    .stChatInput textarea {
        text-align: center !important;
        font-size: 16px !important; /* Evita o zoom automático do iPhone ao clicar */
    }

    /* 4. MEDIA QUERY: Ajustes exclusivos para telas pequenas (Celulares) */
    @media (max-width: 640px) {
        /* Reduz o tamanho da fonte do título no celular */
        h1 {
            font-size: 1.8rem !important;
        }
        /* Ajusta a largura das mensagens para não ficarem muito estreitas */
        .stChatMessage {
            padding: 10px !important;
            margin-bottom: 10px !important;
        }
        /* Centraliza melhor a logo da barra lateral no mobile */
        [data-testid="stSidebar"] img {
            max-width: 80px !important;
        }
    }

    /* 5. Efeito Visual nas Mensagens */
    [data-testid="stChatMessage"] {
        border-radius: 15px;
        background-color: rgba(255, 255, 255, 0.05); /* Um fundo sutil */
        margin-bottom: 15px;
    }
    /* Centralizar o Label e o Texto do File Uploader na Sidebar */
    [data-testid="stSidebar"] .stFileUploader section {
        padding: 0 !important;
    }
    [data-testid="stSidebar"] .stFileUploader label {
        text-align: center !important;
        display: block !important;
        width: 100% !important;
    }
    [data-testid="stSidebar"] .stFileUploader div div {
        display: flex !important;
        justify-content: center !important;
        text-align: center !important;
    }
    
    /* Centralizar o texto de sucesso/erro na sidebar */
    [data-testid="stSidebar"] .stAlert {
        text-align: center !important;
    }

    /* Centralizar o botão de upload (estilo do drag and drop) */
    [data-testid="stSidebar"] section[data-testid="stFileUploadDropzone"] {
        justify-content: center !important;
        text-align: center !important;
    }
</style>
"""

# O comando markdown com unsafe_allow_html=True permite que o CSS funcione
st.markdown(estilo_customizado, unsafe_allow_html=True)

load_dotenv()

# 1. Tenta pegar a chave do Segredo (Nuvem) ou do .env (Local)
# Tenta carregar a chave de forma segura
try:
    if "GEMINI_API_KEY" in st.secrets:
        chave_secreta = st.secrets["GEMINI_API_KEY"]
    else:
        chave_secreta = os.getenv("GEMINI_API_KEY")
except Exception:
    # Se der erro de SecretNotFoundError, tenta o env ou fica None
    chave_secreta = os.getenv("GEMINI_API_KEY", None)

if chave_secreta:
    genai.configure(api_key=chave_secreta)
    modelo_ia = genai.GenerativeModel("gemini-2.5-flash")
    api_configurada = True
else:
    st.error("⚠️ Erro: Chave de API não encontrada. Verifique o secrets.toml ou o arquivo .env")
    api_configurada = False


with st.sidebar:
    st.markdown(
        """
        <div style="display: flex; justify-content: center;">
            <img src="https://cdn-icons-png.flaticon.com/512/4712/4712027.png" width="100">
        </div>
        """, 
        unsafe_allow_html=True
    )
   # --- TEXTOS CENTRALIZADOS COM HTML ---
    st.markdown("<h2 style='text-align: center;'>⚙️ Configurações</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Bem-vindo ao painel do Bitt.ai.</p>", unsafe_allow_html=True)
    
    # --- BOTÃO SIMÉTRICO (Ocupa a largura toda) ---
    if st.button("🗑️ Limpar chat", use_container_width=True):
        st.session_state["lista_mensagens"] = []
        st.rerun()

    st.markdown("<h2 style='text-align: center;'>📁 Documentos</h2>", unsafe_allow_html=True)
    
    # Campo para subir o arquivo
    arquivo_subido = st.file_uploader("Suba um PDF para o Bitt.ai analisar", type="pdf", label_visibility="visible")
    
    if arquivo_subido:
        # Lógica para extrair o texto do PDF
        leitor = PyPDF2.PdfReader(arquivo_subido)
        texto_extraido = ""
        for pagina in leitor.pages:
            texto_extraido += pagina.extract_text()
        
        # Guardamos o texto na "memória" da sessão
        st.session_state["contexto_arquivo"] = texto_extraido
        st.success("✅ Documento lido! Agora pode perguntar sobre ele.")

    st.divider() # Cria uma linha separadora bem sutil
    st.markdown("<div style='text-align: center;'><small>Desenvolvido por <a href='https://github.com/pedrobittencourtdev' target='_blank' style='color: #00E676; text-decoration: none;'>Pedro Bittencourt</a></small></div>", unsafe_allow_html=True)

# Titulo
# --- TÍTULO E SUBTÍTULO CENTRALIZADOS NA PÁGINA PRINCIPAL ---
st.markdown("<h1 style='text-align: center;'>🦉 Bitt.ai</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #a5a5a5; font-size: 14px;'>Assistente Corporativo · Profissional · Preciso</p>", unsafe_allow_html=True)

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
    if not api_configurada:
        st.error("❌ API não configurada.")
    else:
        # 1. Mostra a mensagem do usuário (texto puro)
        st.chat_message("user").write(texto_usuario)
        
        # 2. Prepara o prompt com ou sem PDF
        contexto = st.session_state.get("contexto_arquivo", "")
        if contexto:
            prompt_para_ia = f"CONTEÚDO DO PDF:\n{contexto}\n\nPERGUNTA DO USUÁRIO: {texto_usuario}"
        else:
            prompt_para_ia = texto_usuario

        # 3. Adiciona ao histórico (guardamos o texto original do usuário para a tela não ficar feia)
        st.session_state["lista_mensagens"].append({"role": "user", "content": texto_usuario})

        # 4. Gera resposta
        with st.chat_message("assistant"):
            with st.spinner("Processando..."):
                try:
                    # Enviamos o prompt_para_ia (que contém o PDF) no lugar do texto simples
                    # Para manter o histórico vivo, enviamos a lista e substituímos a última pergunta
                    historico_gemini = []
                    for msg in st.session_state["lista_mensagens"][:-1]:
                        historico_gemini.append({"role": msg["role"], "parts": [msg["content"]]})
                    
                    # Adiciona a pergunta atual turbinada com o PDF
                    historico_gemini.append({"role": "user", "parts": [prompt_para_ia]})

                    resposta_stream = modelo_ia.generate_content(historico_gemini, stream=True)

                    def gerador_de_texto():
                        for chunk in resposta_stream:
                            if chunk.text: yield chunk.text

                    texto_completo = st.write_stream(gerador_de_texto())
                    st.session_state["lista_mensagens"].append({"role": "model", "content": texto_completo})

                except Exception as e:
                    st.error(f"❌ Erro: {e}")