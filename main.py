import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
import PyPDF2
from PIL import Image

# ==========================================
# 1. CONFIGURAÇÕES GERAIS E CSS
# ==========================================
def aplicar_estilos():
    estilo_customizado = """
    <style>
        /* Esconde apenas elementos irrelevantes do topo/rodapé */
        .stDeployButton, footer, .viewerBadge-container {display: none !important;}
        
        /* Ajuste de espaçamento do chat */
        .main .block-container {padding-top: 2rem !important; padding-bottom: 5rem !important;}
        
        /* Estilo das mensagens */
        [data-testid="stChatMessage"] {
            border-radius: 15px; 
            background-color: rgba(255, 255, 255, 0.05); 
            margin-bottom: 15px;
        }

        /* Centralização dos textos dentro da Sidebar */
        [data-testid="stSidebar"] .stMarkdown h1, 
        [data-testid="stSidebar"] .stMarkdown p {
            text-align: center !important;
        }
        
        /* Garante que a sidebar seja visível e tenha uma cor de fundo distinta */
        [data-testid="stSidebar"] {
            background-color: #111 !important;
        }
    </style>
    """
    st.markdown(estilo_customizado, unsafe_allow_html=True)
# ==========================================
# 2. FUNÇÕES DE LÓGICA (BACKEND)
# ==========================================
def configurar_ia():
    # Localiza o .env no mesmo diretório do script
    diretorio_atual = os.path.dirname(os.path.abspath(__file__))
    caminho_env = os.path.join(diretorio_atual, ".env")
    load_dotenv(caminho_env)
    
    chave_secreta = None

    # Tenta carregar a chave (Sua lógica original com melhoria de segurança)
    try:
        if "GEMINI_API_KEY" in st.secrets:
            chave_secreta = st.secrets["GEMINI_API_KEY"]
        else:
            chave_secreta = os.getenv("GEMINI_API_KEY")
    except:
        chave_secreta = os.getenv("GEMINI_API_KEY")

    if chave_secreta:
        # .strip() é vital para evitar o erro 400
        genai.configure(api_key=chave_secreta.strip())
        # gemini-1.5-flash é o modelo mais estável para contas gratuitas
        return genai.GenerativeModel("gemini-2.5-flash"), True
    
    return None, False
    
    return None, False

def extrair_texto_pdf(arquivo):
    leitor = PyPDF2.PdfReader(arquivo)
    return "".join([pagina.extract_text() for pagina in leitor.pages])

# ==========================================
# 3. COMPONENTES DA INTERFACE (SIDEBAR)
# ==========================================
def renderizar_sidebar():
    with st.sidebar:
        st.markdown("<h1 style='text-align: center; font-size: 24px;'>Funções do Bitt.ai</h1>", unsafe_allow_html=True)
        st.divider()

        # --- FERRAMENTAS ---
        with st.expander("⚙️ Ferramentas", expanded=False):
            if st.button("🗑️ Limpar Chat", use_container_width=True, key="btn_limpar_unico"):
                st.session_state.lista_mensagens = []
                st.session_state.pop("contexto_arquivo", None)
                st.session_state.pop("contexto_imagem", None)
                st.rerun()

        # --- PDF ---
        pdf_aberto = "contexto_arquivo" in st.session_state
        with st.expander("📁 Analisar PDF", expanded=pdf_aberto):
            arq_pdf = st.file_uploader("Subir PDF", type="pdf", key="up_pdf", label_visibility="collapsed")
            if arq_pdf:
                st.session_state["contexto_arquivo"] = extrair_texto_pdf(arq_pdf)
                st.success("✅ PDF pronto!")

        # --- IMAGEM ---
        img_aberta = "contexto_imagem" in st.session_state
        with st.expander("🖼️ Analisar Imagem", expanded=img_aberta):
            arq_img = st.file_uploader("Subir Imagem", type=["png","jpg","jpeg"], key="up_img", label_visibility="collapsed")
            if arq_img:
                imagem = Image.open(arq_img)
                st.image(imagem, use_container_width=True)
                st.session_state["contexto_imagem"] = imagem
                st.success("✅ Imagem pronta!")

    # --- PARTE DE SEGURANÇA ---
        st.markdown("---")
        st.markdown(
            """
            <div style="background-color: rgba(0, 230, 118, 0.1); padding: 12px; border-radius: 12px; border: 1px solid rgba(0, 230, 118, 0.2); margin-bottom: 15px;">
                <div style="display: flex; align-items: center; justify-content: center; gap: 8px;">
                    <span style="font-size: 18px;">🛡️</span>
                    <span style="color: #00E676; font-size: 12px; font-weight: bold; text-transform: uppercase; letter-spacing: 1px;">Dados Protegidos</span>
                </div>
                <p style="font-size: 11px; color: #aaa; text-align: center; margin-top: 8px; line-height: 1.3;">
                    Processamento em <b>memória volátil</b>. Arquivos não são armazenados permanentemente.
                </p>
            </div>
            """, 
            unsafe_allow_html=True
        )

        # --- RODAPÉ ---
        st.divider()
        st.markdown("<p style='text-align: center; font-weight: bold;'>👨‍💻 Desenvolvedor</p>", unsafe_allow_html=True)
        st.markdown(f"""
            <div style="background-color: rgba(255,255,255,0.05); padding: 10px; border-radius: 10px; text-align: center; border: 1px solid #00E676;">
                <span style="color: #00E676; font-weight: bold;">Pedro Bittencourt</span><br>
                <small>Estudante de Engenharia de Software</small>
            </div>
        """, unsafe_allow_html=True)

# ==========================================
# 4. EXECUÇÃO PRINCIPAL
# ==========================================
def main():
    # O set_page_config DEVE ser a primeira linha do Streamlit no main
    st.set_page_config(page_title="Bitt.ai", page_icon="🦉", layout="centered")
    
    aplicar_estilos()
    modelo_ia, api_ok = configurar_ia()
    
    if "lista_mensagens" not in st.session_state:
        st.session_state.lista_mensagens = []

    # Chama a sidebar aqui
    renderizar_sidebar()

    # Título Principal
    st.markdown("<h1 style='text-align: center;'>🦉 Bitt.ai</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #888;'>Assistente Inteligente Multimodal</p>", unsafe_allow_html=True)

    # Exibe Histórico
    for msg in st.session_state.lista_mensagens:
        role = "assistant" if msg["role"] == "model" else "user"
        st.chat_message(role).write(msg["content"])

    # Entrada do Usuário
    if prompt_user := st.chat_input("Como posso ajudar?"):
        if not api_ok:
            st.error("Chave de API não configurada corretamente.")
            return

        st.chat_message("user").write(prompt_user)
        st.session_state.lista_mensagens.append({"role": "user", "content": prompt_user})

        # Monta prompt multimodal
        prompt_completo = []
        if "contexto_arquivo" in st.session_state:
            prompt_completo.append(f"CONTEXTO PDF:\n{st.session_state.contexto_arquivo}")
        if "contexto_imagem" in st.session_state:
            prompt_completo.append(st.session_state.contexto_imagem)
        prompt_completo.append(prompt_user)

        # Resposta da IA
        with st.chat_message("assistant"):
            with st.spinner("Pensando..."):
                try:
                    stream = modelo_ia.generate_content(prompt_completo, stream=True)
                    texto_final = st.write_stream(chunk.text for chunk in stream if chunk.text)
                    st.session_state.lista_mensagens.append({"role": "model", "content": texto_final})
                except Exception as e:
                    st.error(f"Erro na IA: {e}")

if __name__ == "__main__":
    main()