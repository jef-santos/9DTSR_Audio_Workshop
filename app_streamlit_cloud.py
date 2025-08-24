import streamlit as st
from io import BytesIO
from gtts import gTTS
from pydub import AudioSegment
import speech_recognition as sr
import tempfile
from unidecode import unidecode

# -------------- Utils --------------

def normalizar(txt: str) -> str:
    if not txt: return ""
    txt = unidecode(txt.lower())
    for ch in ",.;:!?/\\|()[]{}\"'":
        txt = txt.replace(ch, " ")
    return " ".join(txt.split())

def detectar_opcao(texto: str):
    t = normalizar(texto)
    saldo_kw      = {"saldo", "consultar saldo", "conta", "consulta"}
    compra_kw     = {"compra internacional", "simulacao", "simular", "compra", "internacional"}
    atendente_kw  = {"atendente", "pessoa", "humano", "falar com alguem", "falar com atendente"}
    sair_kw       = {"sair", "encerrar", "finalizar", "terminar"}

    def contem(kw): return any(k in t for k in kw)
    if contem(saldo_kw):     return "saldo"
    if contem(compra_kw):    return "compra"
    if contem(atendente_kw): return "atendente"
    if contem(sair_kw):      return "sair"
    return None

def tts_bytes(texto_pt: str) -> bytes:
    """Gera MP3 em memória com gTTS."""
    buf = BytesIO()
    tts = gTTS(text=texto_pt, lang="pt", tld="com.br")
    tts.write_to_fp(buf)
    buf.seek(0)
    return buf.read()

def transcrever_wav_bytes(wav_bytes: bytes) -> str:
    """Transcreve um WAV (bytes) usando SpeechRecognition (Google)."""
    r = sr.Recognizer()
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=True) as tmp:
        tmp.write(wav_bytes)
        tmp.flush()
        with sr.AudioFile(tmp.name) as source:
            audio = r.record(source)
    try:
        return r.recognize_google(audio, language="pt-BR")
    except sr.UnknownValueError:
        return ""
    except Exception:
        return ""

# -------------- UI --------------

st.set_page_config(page_title="QuantumFinance Voice Bot (Cloud)", layout="centered")
st.title("📞 QuantumFinance Voice Bot — Simulação (Cloud)")

st.caption("Grave sua fala no microfone do navegador, eu transcrevo e respondo com áudio. "
           "Nenhum áudio toca no servidor — tudo toca no **seu navegador**.")

# Mensagens fixas
mensagens = {
    "saudacao": (
        "Bem-vindo à QuantumFinance! Pelo navegador, vejo que estou falando com o Jefferson. "
        "Como posso te ajudar hoje? Temos algumas opções disponíveis."
    ),
    "opcoes": (
        "Você pode escolher entre: "
        "Consultar o saldo da sua conta, "
        "Simular uma compra internacional, "
        "Falar com um atendente, "
        "Ou sair do atendimento."
    ),
    "resposta_saldo": (
        "Você escolheu consulta ao saldo da conta. "
        "Para seguir, vou precisar confirmar alguns dos seus dados de segurança, "
        "como CPF e data de nascimento."
    ),
    "resposta_compra": (
        "Você escolheu simulação de compra internacional. "
        "Para realizar a simulação, precisarei que você informe o valor desejado, "
        "o país de destino e a moeda."
    ),
    "resposta_atendente": (
        "Você escolheu falar com um atendente. "
        "Aguarde na linha, estamos conectando você a um dos nossos especialistas."
    ),
    "resposta_sair": (
        "Encerrando o atendimento. "
        "Obrigado por utilizar o serviço de voz da QuantumFinance. "
        "Tenha um ótimo dia, Jefferson!"
    ),
    "nao_identificado": (
        "Desculpe, não consegui entender sua escolha. "
        "Por favor, repita a opção desejada: saldo, compra internacional, atendente ou sair."
    ),
    "retorno_menu": "Fim da simulação, retornando para o menu principal."
}

# Sessão
if "historico" not in st.session_state:
    st.session_state.historico = []
if "encerrado" not in st.session_state:
    st.session_state.encerrado = False

# Saudação + Opções (áudios)
with st.expander("🔊 Saudação e opções", expanded=True):
    st.markdown(f"**Saudação:** {mensagens['saudacao']}")
    st.audio(tts_bytes(mensagens["saudacao"]), format="audio/mp3")
    st.markdown(f"**Opções:** {mensagens['opcoes']}")
    st.audio(tts_bytes(mensagens["opcoes"]), format="audio/mp3")

st.divider()
st.subheader("🎙️ Grave sua opção")

# Componente de gravação (streamlit-audiorec)
from audiorecorder import audiorecorder  # pacote: streamlit-audiorec

audio = audiorecorder("Gravar", "Parar")  # retorna objeto com bytes WAV quando para

col1, col2, col3, col4 = st.columns(4)
btn_saldo = col1.button("Saldo")
btn_compra = col2.button("Compra internacional")
btn_atend = col3.button("Atendente")
btn_sair  = col4.button("Sair")

texto_usuario = ""
forcado = None

if audio and len(audio) > 0:
    # O componente retorna áudio em WAV PCM already; garantimos bytes
    wav_bytes = audio.tobytes()
    # Opcional: re-encode com pydub para garantir formato consistente
    seg = AudioSegment.from_file(BytesIO(wav_bytes), format="wav")
    out_buf = BytesIO()
    seg.export(out_buf, format="wav")
    out_wav = out_buf.getvalue()

    texto_usuario = transcrever_wav_bytes(out_wav)
    if texto_usuario:
        st.success(f"Você disse: _{texto_usuario}_")
    else:
        st.warning("Não consegui entender sua fala. Tente de novo.")

# Botões como fallback de acessibilidade
if btn_saldo:   forcado = "saldo"
if btn_compra:  forcado = "compra"
if btn_atend:   forcado = "atendente"
if btn_sair:    forcado = "sair"

if forcado:
    opc = forcado
else:
    opc = detectar_opcao(texto_usuario) if texto_usuario else None

st.divider()
st.subheader("📣 Resposta")

if opc == "saldo":
    st.audio(tts_bytes(mensagens["resposta_saldo"]), format="audio/mp3")
    st.audio(tts_bytes(mensagens["retorno_menu"]), format="audio/mp3")
    st.audio(tts_bytes(mensagens["opcoes"]), format="audio/mp3")

elif opc == "compra":
    st.audio(tts_bytes(mensagens["resposta_compra"]), format="audio/mp3")
    st.audio(tts_bytes(mensagens["retorno_menu"]), format="audio/mp3")
    st.audio(tts_bytes(mensagens["opcoes"]), format="audio/mp3")

elif opc == "atendente":
    st.audio(tts_bytes(mensagens["resposta_atendente"]), format="audio/mp3")
    st.audio(tts_bytes(mensagens["retorno_menu"]), format="audio/mp3")
    st.audio(tts_bytes(mensagens["opcoes"]), format="audio/mp3")

elif opc == "sair":
    st.audio(tts_bytes(mensagens["resposta_sair"]), format="audio/mp3")
    st.session_state.encerrado = True

elif texto_usuario != "":
    # Falou algo mas não mapeou
    st.audio(tts_bytes(mensagens["nao_identificado"]), format="audio/mp3")
    st.audio(tts_bytes(mensagens["opcoes"]), format="audio/mp3")

# Histórico (opcional)
if texto_usuario:
    st.session_state.historico.append({"user": texto_usuario, "opc": opc or "indefinido"})

with st.expander("📝 Histórico (sessão)"):
    if st.session_state.historico:
        for i, h in enumerate(st.session_state.historico, 1):
            st.write(f"{i}. Você: _{h['user']}_ → opção: **{h['opc']}**")
    else:
        st.caption("Sem interações ainda.")
