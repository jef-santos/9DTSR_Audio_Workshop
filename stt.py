import logging
import tempfile
import speech_recognition as sr

def _try_pyaudio_stt(r: sr.Recognizer, timeout=6.0, phrase_time_limit=6.0):
    try:
        with sr.Microphone() as source:
            logging.info("[STT] Ajustando ruído (PyAudio)...")
            r.adjust_for_ambient_noise(source, duration=0.6)
            logging.info("[STT] Aguardando fala (PyAudio)...")
            audio = r.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
        texto = r.recognize_google(audio, language="pt-BR")
        logging.info("[STT] Transcrição (PyAudio): %s", texto)
        return texto
    except Exception as e:
        logging.warning("[STT] PyAudio indisponível/erro: %s", e)
        return None

def _sounddevice_stt(r: sr.Recognizer, seconds=6, samplerate=16000):
    import sounddevice as sd
    import soundfile as sf

    logging.info(f"[STT] Gravando com sounddevice por {seconds}s...")
    audio = sd.rec(int(seconds * samplerate), samplerate=samplerate, channels=1, dtype="int16")
    sd.wait()

    with tempfile.NamedTemporaryFile(suffix=".wav", delete=True) as tmp:
        sf.write(tmp.name, audio, samplerate)
        with sr.AudioFile(tmp.name) as source:
            data = r.record(source)
        texto = r.recognize_google(data, language="pt-BR")
        logging.info("[STT] Transcrição (sounddevice): %s", texto)
        return texto

def transcrever_audio(mic_index: int | None = None,
                      timeout: float = 6.0,
                      phrase_time_limit: float = 6.0) -> str:
    r = sr.Recognizer()

    # 1) tenta microfone nativo (PyAudio). Se falhar, cai pro fallback.
    texto = _try_pyaudio_stt(r, timeout, phrase_time_limit)
    if texto:
        return texto

    # 2) fallback por gravação de janela com sounddevice
    try:
        segundos = min(timeout, phrase_time_limit)
        return _sounddevice_stt(r, seconds=segundos)
    except sr.UnknownValueError:
        logging.warning("[STT] Não foi possível entender o áudio (sounddevice).")
        return ""
    except Exception as e:
        logging.error(f"[STT] Erro no fallback com sounddevice: {e}")
        return ""
