Multi-Agent Research System

This repository contains code for experimenting with multi-agent research systems.

Quick start

1. Copy `.env.example` to `.env` and fill values (do NOT put real API keys in the repository).
2. Create a virtual environment and install dependencies:

```
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

3. Run the app (example):

```
streamlit run app.py
```

Pushing to GitHub

Replace `USERNAME` with your GitHub username and run:

```
git remote add origin https://github.com/USERNAME/Multi-AI-Agent-Research-System.git
git push -u origin main
```

Security note

- Never commit `.env` or API keys. Use `.env.example` to show required variables without secrets.
