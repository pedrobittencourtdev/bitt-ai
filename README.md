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
git clone https://github.com/pedrobittencourtdev/bitt-ai.git
cd bitt-ai

### 2. Instale as dependências

* Certifique-se de ter o Python instalado. É recomendado usar um ambiente virtual (venv).

```bash
pip install streamlit google-generativeai python-dotenv

### 3. Configure a sua Chave de API

***Crie uma chave de API gratuita no Google AI Studio.***

***Na raiz do projeto, crie um arquivo chamado .env (não esqueça do ponto).***

***Adicione a sua chave dentro do arquivo neste formato (sem aspas)***

```bash
GEMINI_API_KEY=sua_chave_api_aqui

### 4. Rode a aplicação
```bash
streamlit run main.py

***O projeto abrirá automaticamente no seu navegador padrão.***

```bash
Desenvolvido por Pedro Bittencourt.