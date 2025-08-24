import os, logging
from datetime import datetime
from unidecode import unidecode


def setup_logs(log_path: str = "quantumvoice.log"):
    # evita handlers duplicados ao rerrodar
    for h in list(logging.root.handlers):
        logging.root.removeHandler(h)

    log_dir = os.path.dirname(log_path) or "."
    os.makedirs(log_dir, exist_ok=True)

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(log_path, encoding="utf-8")
        ]
    )

def garantir_pasta(path: str):
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)

def normalizar(txt: str) -> str:
    """lower + remove acentos + tira pontuação básica."""
    if not txt:
        return ""
    txt = unidecode(txt.lower())
    # simples limpeza (mantemos espaços)
    for ch in ",.;:!?/\\|()[]{}\"'":
        txt = txt.replace(ch, " ")
    return " ".join(txt.split())

def detectar_opcao(texto: str) -> str | None:
    """
    Retorna um dos rótulos: 'saldo', 'compra', 'atendente', 'sair' ou None.
    Precisa reconhecer por PALAVRA-CHAVE (não só números).
    """
    t = normalizar(texto)

    # Palavras-chave (pode ajustar depois se quiser)
    saldo_kw      = {"saldo", "consultar saldo", "conta", "consulta"}
    compra_kw     = {"compra internacional", "simulacao", "simular", "compra", "internacional"}
    atendente_kw  = {"atendente", "pessoa", "humano", "falar com alguem", "falar com atendente"}
    sair_kw       = {"sair", "encerrar", "finalizar", "terminar"}

    def contem(kw_set: set[str]) -> bool:
        return any(k in t for k in kw_set)

    if contem(saldo_kw):     return "saldo"
    if contem(compra_kw):    return "compra"
    if contem(atendente_kw): return "atendente"
    if contem(sair_kw):      return "sair"

    return None