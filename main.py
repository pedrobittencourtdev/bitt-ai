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
    # 1. Logo e Título Principal (Mantidos no topo)
    st.markdown(
        """
        <div style="display: flex; justify-content: center; margin-bottom: 20px;">
            <img src="https://cdn-icons-png.flaticon.com/512/4712/4712027.png" width="80">
        </div>
        """, 
        unsafe_allow_html=True
    )
    st.markdown("<h1 style='text-align: center; font-size: 24px;'>Painel Bitt.ai</h1>", unsafe_allow_html=True)
    st.divider() # Linha separadora sutil

    # --- 2. GRUPO DE CONFIGURAÇÕES (RETRÁTIL) ---
    with st.expander("⚙️ Ferramentas do Chat", expanded=False): # Começa fechado
        st.markdown("<p style='text-align: center; color: #a5a5a5;'>Gerencie sua sessão atual.</p>", unsafe_allow_html=True)
        # O botão agora ocupa a largura total dentro do expander
        if st.button("🗑️ Limpar Conversa", use_container_width=True):
            st.session_state["lista_mensagens"] = []
            if "contexto_arquivo" in st.session_state:
                del st.session_state["contexto_arquivo"] # Limpa o arquivo da memória também
            st.rerun()

    # --- 3. GRUPO DE DOCUMENTOS (RETRÁTIL) ---
    # Este expander começa aberto se o usuário já subiu um arquivo
    expander_docs_aberto = True if "contexto_arquivo" in st.session_state else False
    with st.expander("📁 Analisar PDF", expanded=expander_docs_aberto):
        st.markdown("<p style='text-align: center; color: #a5a5a5;'>Suba um documento para contextualizar a IA.</p>", unsafe_allow_html=True)
        
        # O componente de upload, centralizado pelo CSS que já criamos
        arquivo_subido = st.file_uploader("Selecione um arquivo PDF", type="pdf", label_visibility="collapsed")
        
        if arquivo_subido:
            # Lógica de extração (Sua lógica original, mais limpa)
            leitor = PyPDF2.PdfReader(arquivo_subido)
            texto_extraido = "".join([pagina.extract_text() for pagina in leitor.pages])
            st.session_state["contexto_arquivo"] = texto_extraido
            st.success("✅ PDF carregado na memória!")

    # --- 4. RODAPÉ (RETRÁTIL E SUTIL) ---
    st.sidebar.markdown("---") # Linha divisória firme
    st.markdown("<p style='text-align: center; font-weight: bold; margin-bottom: 5px;'>👨‍💻 Desenvolvedor</p>", unsafe_allow_html=True)
    
    # Card do Desenvolvedor
    st.markdown(
        """
        <div style="background-color: rgba(255, 255, 255, 0.05); padding: 15px; border-radius: 15px; text-align: center; border: 1px solid rgba(0, 230, 118, 0.3);">
            <span style="color: #00E676; font-size: 16px; font-weight: bold;">Pedro Bittencourt</span><br>
            <p style="font-size: 12px; color: #aaa; margin-top: 5px;">Estudante de Engenharia de software</p>
            <a href="https://github.com/pedrobittencourtdev" target="_blank" 
               style="background-color: #00E676; color: black; padding: 5px 15px; border-radius: 20px; text-decoration: none; font-size: 12px; font-weight: bold; display: inline-block; margin-top: 10px;">
               Ver Portfólio
            </a>
        </div>
        """, 
        unsafe_allow_html=True
    )
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