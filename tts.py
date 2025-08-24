import logging
from gtts import gTTS

def gerar_audio(texto: str, filename: str) -> str:
    """Gera áudio TTS (mp3) com gTTS e salva no filename."""
    try:
        tts = gTTS(text=texto, lang="pt")
        tts.save(filename)
        logging.info(f"[TTS] Áudio gerado: {filename}")
        return filename
    except Exception as e:
        logging.error(f"[TTS] Erro ao gerar áudio: {e}")
        return ""
