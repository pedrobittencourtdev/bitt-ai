<div align="center">

# 🤖 Bitt.ai

**Um chatbot inteligente e conversacional powered by Google Gemini**

[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat-square&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Google Gemini](https://img.shields.io/badge/Google%20Gemini-4285F4?style=flat-square&logo=google&logoColor=white)](https://ai.google.dev/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](LICENSE)

[Demo](#) · [Reportar Bug](https://github.com/pedrobittencourtdev/bitt-ai/issues) · [Sugerir Feature](https://github.com/pedrobittencourtdev/bitt-ai/issues)

</div>

---

## 📌 Sobre o Projeto

O **Bitt.ai** é um chatbot interativo construído com Python e Streamlit, integrado ao modelo `gemini-2.5-flash` do Google. O projeto oferece uma interface de chat limpa e fluida, com memória de conversa em tempo real e gerenciamento seguro de credenciais.

> Ideal como ponto de partida para quem quer explorar IA generativa em aplicações web com Python.

---

## ✨ Funcionalidades

- 💬 **Interface fluida** — Chat responsivo e intuitivo construído com Streamlit
- 🧠 **Memória contextual** — O bot mantém o contexto da conversa usando `session_state`
- ⚡ **Respostas inteligentes** — Powered by `gemini-2.5-flash`, modelo rápido e preciso do Google
- 🔐 **Credenciais seguras** — Chave de API protegida via variáveis de ambiente (`.env`)

---

## 🛠️ Tecnologias

| Tecnologia | Descrição |
|---|---|
| [Python](https://www.python.org/) | Linguagem base do projeto |
| [Streamlit](https://streamlit.io/) | Interface web e gerenciamento de estado |
| [Google Generative AI SDK](https://ai.google.dev/) | Comunicação com o modelo Gemini |
| [python-dotenv](https://pypi.org/project/python-dotenv/) | Gerenciamento de variáveis de ambiente |

---

## 🚀 Como executar localmente

### Pré-requisitos

- Python 3.8+
- Uma chave de API do Google Gemini ([obtenha aqui gratuitamente](https://aistudio.google.com/app/apikey))

### Passo a passo

**1. Clone o repositório**
```bash
git clone https://github.com/pedrobittencourtdev/bitt-ai.git
cd bitt-ai
```

**2. Crie e ative um ambiente virtual** *(recomendado)*
```bash
# Linux / macOS
python -m venv venv && source venv/bin/activate

# Windows
python -m venv venv && venv\Scripts\activate
```

**3. Instale as dependências**
```bash
pip install streamlit google-generativeai python-dotenv
```

**4. Configure a chave de API**

Crie um arquivo `.env` na raiz do projeto e adicione sua chave:
```env
GEMINI_API_KEY=sua_chave_api_aqui
```

> ⚠️ **Nunca commite o arquivo `.env`**. Certifique-se de que ele está no seu `.gitignore`.

**5. Execute a aplicação**
```bash
streamlit run main.py
```

A aplicação abrirá automaticamente em `http://localhost:8501`.

---

## 📁 Estrutura do Projeto

```
bitt-ai/
├── main.py          # Aplicação principal
├── .env             # Variáveis de ambiente (não versionado)
├── .env.example     # Exemplo de configuração
├── .gitignore
└── README.md
```

---

## 🤝 Contribuindo

Contribuições são bem-vindas! Sinta-se à vontade para abrir uma [issue](https://github.com/pedrobittencourtdev/bitt-ai/issues) ou enviar um pull request.

1. Faça um fork do projeto
2. Crie sua branch: `git checkout -b feature/minha-feature`
3. Commit suas mudanças: `git commit -m 'feat: minha nova feature'`
4. Push para a branch: `git push origin feature/minha-feature`
5. Abra um Pull Request

---

## 📄 Licença

Distribuído sob a licença MIT. Veja [`LICENSE`](LICENSE) para mais informações.

---

<div align="center">
  Desenvolvido com ❤️ por <a href="https://github.com/pedrobittencourtdev">Pedro Bittencourt</a>
</div>