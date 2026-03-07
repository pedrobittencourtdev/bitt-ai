# Bitt.ai 🤖

Um ChatBot interativo e inteligente construído com Python, Streamlit e a API do Google Gemini. Este projeto demonstra a integração de modelos de Inteligência Artificial Generativa em uma interface web simples e amigável, mantendo o histórico de conversação do usuário em tempo real.

## 🚀 Funcionalidades

* **Interface Web Fluida:** Interface de chat limpa e responsiva construída com Streamlit.
* **Memória de Conversa:** O bot lembra do contexto da conversa atual usando o `session_state` do Streamlit.
* **Integração com IA:** Respostas rápidas e precisas geradas pelo modelo `gemini-2.5-flash` do Google.
* **Segurança de Credenciais:** Uso de variáveis de ambiente (`.env`) para proteger a chave de API.

## 🛠️ Tecnologias Utilizadas

* [Python](https://www.python.org/)
* [Streamlit](https://streamlit.io/) (Front-end e gerenciamento de estado)
* [Google Generative AI SDK](https://ai.google.dev/) (Comunicação com o Gemini)
* [python-dotenv](https://pypi.org/project/python-dotenv/) (Gerenciamento de variáveis de ambiente)

## ⚙️ Como executar o projeto localmente

Siga os passos abaixo para rodar o Bitt.ai na sua máquina:

### 1. Clone o repositório
```bash
