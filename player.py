import logging, time, pygame

# inicializa uma vez só
if not pygame.mixer.get_init():
    pygame.mixer.init()

def tocar_audio(filename: str):
    """Reproduz um arquivo de áudio (mp3/wav) de forma bloqueante."""
    try:
        logging.info(f"[PLAYER] Reproduzindo: {filename}")
        pygame.mixer.music.load(filename)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            time.sleep(0.05)
        logging.info(f"[PLAYER] Finalizado: {filename}")
    except Exception as e:
        logging.error(f"[PLAYER] Erro ao reproduzir áudio: {e}")

def parar():
    """Para reprodução atual (se precisar)."""
    try:
        pygame.mixer.music.stop()
    except Exception:
        pass

