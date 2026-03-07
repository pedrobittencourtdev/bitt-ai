import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
import datetime

# ─────────────────────────────────────────────
#  CONFIGURAÇÃO DA PÁGINA
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Bitt.ai",
    page_icon="🦉",
    layout="centered"
)

# ─────────────────────────────────────────────
#  CSS CUSTOMIZADO
# ─────────────────────────────────────────────
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

# ─────────────────────────────────────────────
#  VARIÁVEIS E CONFIGURAÇÕES
# ─────────────────────────────────────────────
load_dotenv()

SYSTEM_PROMPT = """Você é Bitt.ai, um assistente virtual corporativo de alta performance.

Diretrizes de comportamento:
- Comunique-se de forma clara, objetiva e profissional, sem jargões desnecessários.
- Estruture suas respostas com lógica e precisão.
- Ao lidar com problemas complexos, apresente análises estruturadas com pontos principais.
- Seja direto e conciso — respeite o tempo do usuário.
- Evite respostas vagas. Prefira dados, fatos e exemplos concretos quando possível.
- Mantenha um tom formal, mas acessível. Nunca seja rígido ou robótico.
- Quando não souber algo, declare com clareza e ofereça o melhor caminho alternativo.
- Finalize respostas longas com um resumo ou próximos passos quando aplicável.

Você representa excelência profissional em cada interação."""

# ─────────────────────────────────────────────
#  INICIALIZAÇÃO DA API
# ─────────────────────────────────────────────
chave_secreta = os.getenv("GEMINI_API_KEY")
api_configurada = False

if not chave_secreta:
    st.error("⚠️ **Chave de API não encontrada.** Verifique se o arquivo `.env` contém `GEMINI_API_KEY`.")
else:
    try:
        genai.configure(api_key=chave_secreta)
        modelo_ia = genai.GenerativeModel("gemini-2.5-flash")
        api_configurada = True
    except Exception as e:
        st.error(f"⚠️ **Erro ao configurar a API:** {e}")

# ─────────────────────────────────────────────
#  SESSION STATE
# ─────────────────────────────────────────────
if "lista_mensagens" not in st.session_state:
    st.session_state["lista_mensagens"] = []

if "total_interacoes" not in st.session_state:
    st.session_state["total_interacoes"] = 0

if "sessao_inicio" not in st.session_state:
    st.session_state["sessao_inicio"] = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")

# ─────────────────────────────────────────────
#  SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/4712/4712027.png", width=80)
    st.markdown("## Bitt.ai")
    st.markdown("*Assistente Corporativo*")
    st.divider()

    st.markdown("#### 📊 Sessão Atual")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Mensagens", len(st.session_state["lista_mensagens"]))
    with col2:
        st.metric("Trocas", st.session_state["total_interacoes"])
    st.caption(f"Início: {st.session_state['sessao_inicio']}")

    st.divider()

    st.markdown("#### ⚙️ Controles")

    # Botão limpar conversa
    if st.button("🗑️ Limpar Conversa"):
        st.session_state["lista_mensagens"] = []
        st.session_state["total_interacoes"] = 0
        st.session_state["sessao_inicio"] = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
        st.rerun()

    # Exportar conversa
    if st.session_state["lista_mensagens"]:
        linhas = [f"BITT.AI — Exportação de Conversa\n{'='*40}\n"]
        linhas.append(f"Data: {st.session_state['sessao_inicio']}\n\n")
        for msg in st.session_state["lista_mensagens"]:
            papel = "Usuário" if msg["role"] == "user" else "Bitt.ai"
            linhas.append(f"[{papel}]\n{msg['content']}\n\n")
        conteudo_export = "".join(linhas)

        st.download_button(
            label="📥 Exportar Conversa (.txt)",
            data=conteudo_export.encode("utf-8"),
            file_name=f"bitt_ai_{datetime.datetime.now().strftime('%Y%m%d_%H%M')}.txt",
            mime="text/plain"
        )

    st.divider()
    st.caption("Bitt.ai v2.0 · Powered by Gemini")

# ─────────────────────────────────────────────
#  INTERFACE PRINCIPAL
# ─────────────────────────────────────────────
st.title("🦉 Bitt.ai")
st.caption("Assistente Corporativo · Profissional · Preciso")

# Mensagem de boas-vindas
if not st.session_state["lista_mensagens"]:
    with st.chat_message("assistant"):
        st.write(
            "Olá. Sou o **Bitt.ai**, seu assistente corporativo. "
            "Estou pronto para auxiliar com análises, redação profissional, "
            "pesquisa e resolução de problemas. Como posso ajudá-lo hoje?"
        )

# Histórico de mensagens
for mensagem in st.session_state["lista_mensagens"]:
    icone = "assistant" if mensagem["role"] == "model" else "user"
    st.chat_message(icone).write(mensagem["content"])

# ─────────────────────────────────────────────
#  INPUT E RESPOSTA
# ─────────────────────────────────────────────
texto_usuario = st.chat_input("Digite sua mensagem...")

if texto_usuario and api_configurada:
    # Exibe mensagem do usuário
    st.chat_message("user").write(texto_usuario)
    st.session_state["lista_mensagens"].append({"role": "user", "content": texto_usuario})

    # Monta histórico no formato Gemini com system prompt
    historico_gemini = [{"role": "user", "parts": [SYSTEM_PROMPT]},
                        {"role": "model", "parts": ["Entendido. Estou pronto para operar conforme as diretrizes definidas."]}]

    for msg in st.session_state["lista_mensagens"]:
        historico_gemini.append({"role": msg["role"], "parts": [msg["content"]]})

    # Streaming da resposta com spinner
    with st.chat_message("assistant"):
        with st.spinner("Processando..."):
            try:
                resposta_stream = modelo_ia.generate_content(
                    historico_gemini,
                    stream=True
                )

                texto_completo = ""
                placeholder = st.empty()

                for chunk in resposta_stream:
                    if chunk.text:
                        texto_completo += chunk.text
                        placeholder.markdown(texto_completo + "▌")  # cursor piscante

                placeholder.markdown(texto_completo)  # versão final sem cursor

                # Salva no histórico
                st.session_state["lista_mensagens"].append(
                    {"role": "model", "content": texto_completo}
                )
                st.session_state["total_interacoes"] += 1

            except genai.types.generation_types.BlockedPromptException:
                st.warning("⚠️ Esta mensagem foi bloqueada pelas políticas de segurança da API.")
            except Exception as e:
                st.error(f"❌ **Erro ao processar a resposta:** {e}")

elif texto_usuario and not api_configurada:
    st.error("❌ Não é possível enviar mensagens sem uma chave de API válida.")