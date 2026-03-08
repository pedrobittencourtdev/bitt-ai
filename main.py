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
        .stDeployButton, footer, .viewerBadge-container {display: none !important;}
        .main .block-container {padding-top: 2rem !important; padding-bottom: 5rem !important;}
        [data-testid="stChatMessage"] {border-radius: 15px; background-color: rgba(255, 255, 255, 0.05); margin-bottom: 15px;}
        [data-testid="stSidebar"] .stMarkdown h1, [data-testid="stSidebar"] .stMarkdown p {text-align: center !important;}
        [data-testid="stSidebar"] {background-color: #111 !important;}
    </style>
    """
    st.markdown(estilo_customizado, unsafe_allow_html=True)

# ==========================================
# 2. FUNÇÕES DE LÓGICA (BACKEND)
# ==========================================
def configurar_ia():
    diretorio_atual = os.path.dirname(os.path.abspath(__file__))
    caminho_env = os.path.join(diretorio_atual, ".env")
    load_dotenv(caminho_env)
    
    chave_secreta = None
    # Tentativa segura de ler segredos sem travar o app
    try:
        if hasattr(st, "secrets") and "GEMINI_API_KEY" in st.secrets:
            chave_secreta = st.secrets["GEMINI_API_KEY"]
    except:
        pass

    if not chave_secreta:
        chave_secreta = os.getenv("GEMINI_API_KEY")

    if chave_secreta:
        genai.configure(api_key=chave_secreta.strip())
        return genai.GenerativeModel("gemini-2.5-flash"), True
    
    return None, False

def extrair_texto_pdf(arquivo):
    try:
        leitor = PyPDF2.PdfReader(arquivo)
        return "".join([pagina.extract_text() for pagina in leitor.pages])
    except: return ""

# ==========================================
# 3. COMPONENTES DA INTERFACE (SIDEBAR)
# ==========================================
def renderizar_sidebar():
    with st.sidebar:
        st.markdown("<h1 style='font-size: 24px;'>Funções do Bitt.ai</h1>", unsafe_allow_html=True)
        st.divider()

        if "uploader_key" not in st.session_state:
            st.session_state.uploader_key = 0

        # --- FERRAMENTAS ---
        with st.expander("⚙️ Ferramentas", expanded=False):
            if st.button("🗑️ Limpar Conversa", use_container_width=True):
                st.session_state.lista_mensagens = []
                st.session_state.pop("temp_pdf", None)
                st.session_state.pop("temp_img", None)
                st.rerun()

        # --- PDF ---
        with st.expander("📁 Analisar PDF", expanded=False):
            arq_pdf = st.file_uploader("Subir PDF", type="pdf", key=f"pdf_{st.session_state.uploader_key}", label_visibility="collapsed")
            if arq_pdf:
                st.session_state["temp_pdf"] = extrair_texto_pdf(arq_pdf)
                st.success("✅ PDF pronto!")

        # --- IMAGEM ---
        with st.expander("🖼️ Analisar Imagem", expanded=False):
            arq_img = st.file_uploader("Subir Imagem", type=["png","jpg","jpeg"], key=f"img_{st.session_state.uploader_key}", label_visibility="collapsed")
            if arq_img:
                img = Image.open(arq_img)
                if img.width > 1200: img.thumbnail((1200, 1200))
                st.session_state["temp_img"] = img
                st.image(img, use_container_width=True)
                st.success("✅ Imagem pronta!")

        # --- PARTE DE SEGURANÇA ---
        st.markdown("""
            <div style="background-color: rgba(0, 230, 118, 0.1); padding: 12px; border-radius: 12px; border: 1px solid rgba(0, 230, 118, 0.2); margin-bottom: 15px;">
                <div style="display: flex; align-items: center; justify-content: center; gap: 8px;">
                    <span style="font-size: 18px;">🛡️</span>
                    <span style="color: #00E676; font-size: 12px; font-weight: bold; text-transform: uppercase;">Dados Protegidos</span>
                </div>
                <p style="font-size: 11px; color: #aaa; text-align: center; margin-top: 8px;">Processamento em memória volátil. Arquivos não são armazenados permanentemente.</p>
            </div>
            """, unsafe_allow_html=True)

        # --- CRÉDITOS ---
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
    st.set_page_config(page_title="Bitt.ai", page_icon="🦉", layout="centered")
    if "lista_mensagens" not in st.session_state:
        st.session_state.lista_mensagens = []
    
    aplicar_estilos()
    renderizar_sidebar()
    modelo_ia, api_ok = configurar_ia()

    st.markdown("<h1 style='text-align: center;'>🦉 Bitt.ai</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #888;'>Assistente Inteligente Multimodal</p>", unsafe_allow_html=True)

    # Exibe Histórico
    for msg in st.session_state.lista_mensagens:
        role = "assistant" if msg["role"] == "model" else "user"
        st.chat_message(role).write(msg["content"])

    if prompt_user := st.chat_input("Como posso ajudar?"):
        if not api_ok: return st.error("⚠️ Erro: Chave de API não configurada corretamente.")

        st.chat_message("user").write(prompt_user)
        
        # Montagem do Contexto
        contexto_envio = []
        for m in st.session_state.lista_mensagens[-6:]:
            contexto_envio.append(f"{m['role']}: {m['content']}")

        # Agrega arquivos temporários ao prompt desta rodada
        prompt_final = prompt_user
        if "temp_pdf" in st.session_state:
            prompt_final += f"\n\n[Contexto do PDF anexado]: {st.session_state.temp_pdf}"
        if "temp_img" in st.session_state:
            contexto_envio.append(st.session_state.temp_img) # Imagem como objeto multimídia

        contexto_envio.append(f"user: {prompt_final}")
        st.session_state.lista_mensagens.append({"role": "user", "content": prompt_user})

        with st.chat_message("assistant"):
            
            placeholder = st.empty()
            with st.spinner("Bitt.ai está processando..."):
                try:
                    # 1. Envia para a IA
                    stream = modelo_ia.generate_content(contexto_envio, stream=True)
                    
                    # 2. Renderiza a resposta com efeito de digitação
                    texto_final = st.write_stream(chunk.text for chunk in stream if chunk.text)
                    
                    # 3. Salva no histórico
                    st.session_state.lista_mensagens.append({"role": "model", "content": texto_final})
                    
                    # 4. LIMPEZA (Apenas após a IA terminar de escrever tudo)
                    if "temp_pdf" in st.session_state or "temp_img" in st.session_state:
                        st.session_state.pop("temp_pdf", None)
                        st.session_state.pop("temp_img", None)
                        st.session_state.uploader_key += 1 
                        st.rerun() 
                
                except Exception as e:
                    st.error(f"Erro na IA: {e}")

if __name__ == "__main__":
    main()