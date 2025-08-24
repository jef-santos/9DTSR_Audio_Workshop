# app_streamlit.py
import streamlit as st
import subprocess
import os
import time
from pathlib import Path

st.set_page_config(page_title="QuantumFinance Voice Bot - Simulação", layout="centered")
st.title("📞 QuantumFinance Voice Bot — Simulação de Ligação")

APP_CMD = ["python", "app.py"]      # ou ["python3", "app.py"] se preferir
LOG_FILE = Path("quantumvoice.log") # mesmo caminho usado no utils.setup_logs


# Estado da sessão
if "proc" not in st.session_state:
    st.session_state.proc = None
if "is_running" not in st.session_state:
    st.session_state.is_running = False

# --- Ações ---
col1, col2 = st.columns(2)
with col1:
    start = st.button("▶️ Iniciar simulação")
with col2:
    stop = st.button("⏹️ Encerrar simulação", type="secondary")

# Iniciar subprocesso
if start and not st.session_state.is_running:
    # limpa log anterior opcionalmente
    try:
        if LOG_FILE.exists():
            LOG_FILE.unlink()
    except Exception:
        pass

    # inicia o app.py em segundo plano (áudio e microfone acontecem na máquina local)
    st.session_state.proc = subprocess.Popen(
        APP_CMD,
        stdout=subprocess.DEVNULL,  # stdout fica no arquivo de log via logging
        stderr=subprocess.STDOUT
    )
    st.session_state.is_running = True
    st.toast("Simulação iniciada. Use o microfone normalmente; o áudio tocará pelo sistema.", icon="✅")

# Encerrar subprocesso
if stop and st.session_state.is_running and st.session_state.proc:
    try:
        st.session_state.proc.terminate()
        st.session_state.proc = None
        st.session_state.is_running = False
        st.toast("Simulação encerrada.", icon="🛑")
    except Exception as e:
        st.error(f"Erro ao encerrar: {e}")

# Detecção de término inesperado (ex.: usuário escolheu 'sair' no app.py)
if st.session_state.is_running and st.session_state.proc and (st.session_state.proc.poll() is not None):
    st.session_state.is_running = False
    st.session_state.proc = None
    st.toast("Simulação finalizada pelo app (opção 'sair').", icon="ℹ️")

st.divider()

# --- Status ---
status = "🟢 Em execução" if st.session_state.is_running else "⚪ Parado"
st.subheader(f"Status: {status}")

st.caption("Dica: ao iniciar, o app local vai tocar os áudios e ouvir seu microfone. "
           "Controle tudo por aqui e acompanhe os logs abaixo.")

# --- Painel de logs com auto-refresh ---
log_placeholder = st.empty()

def read_logs_tail(path: Path, max_bytes: int = 50_000) -> str:
    """Lê o final do arquivo de log (até max_bytes)."""
    if not path.exists():
        return "(sem registros ainda)"
    try:
        size = path.stat().st_size
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            if size > max_bytes:
                f.seek(size - max_bytes)
            return f.read()
    except Exception as e:
        return f"(erro ao ler log: {e})"

# Atualiza logs por ~10s quando em execução; ao clicar em iniciar/encerrar, o script reroda.
if st.session_state.is_running:
    for _ in range(100):  # ~100 iterações -> ~10s de auto-refresh
        logs = read_logs_tail(LOG_FILE)
        log_placeholder.code(logs, language="log")
        time.sleep(0.1)
        # checa se o processo terminou durante a leitura
        if st.session_state.proc and (st.session_state.proc.poll() is not None):
            st.session_state.is_running = False
            st.session_state.proc = None
            break
    # último refresh após o loop
    logs = read_logs_tail(LOG_FILE)
    log_placeholder.code(logs, language="log")
else:
    logs = read_logs_tail(LOG_FILE)
    log_placeholder.code(logs, language="log")

st.divider()
st.markdown("**Como usar**")
st.markdown("""
1. Clique **Iniciar simulação**.  
2. O app vai tocar a saudação e o menu. Fale sua escolha (ex.: "saldo", "compra internacional", "atendente" ou "sair").  
3. Acompanhe os **logs** e, quando quiser, clique **Encerrar simulação** aqui no painel.
""")
