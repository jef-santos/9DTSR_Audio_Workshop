import os, logging
from tts import gerar_audio
from stt import transcrever_audio
from player import tocar_audio
from utils import setup_logs, garantir_pasta, detectar_opcao

AUDIO_DIR = "audios"

def preparar_mensagens() -> dict[str, str]:
    return {
        "saudacao": (
        "Bem-vindo à QuantumFinance! Pelo telefone, vejo que estou falando com o Jefferson."
        "Como posso te ajudar hoje? Temos algumas opções disponíveis."
        ),

        "opcoes": (
            "Você pode escolher entre: "
            "Consultar ao saldo da conta. "
            "Simular uma compra internacional. "
            "Falar com um atendente. "
            "Sair do atendimento."
        ),

        "resposta_saldo": (
            "Você escolheu consulta ao saldo da conta. "
            "Para seguir, vou precisar confirmar alguns dos seus dados de segurança. "
            "Por favor, tenha em mãos seu CPF e data de nascimento."
            "Fim da simulação, retornando para o menu principal."
        ),

        "resposta_compra": (
            "Você escolheu simulação de compra internacional. "
            "Para realizar a simulação, precisarei que você informe o valor desejado em reais, "
            "o país de destino e a moeda para a qual deseja converter. "
            "Essas informações vão ajudar a calcular as taxas e o custo total da operação."
            "Fim da simulação, retornando para o menu principal."
        ),

        "resposta_atendente": (
            "Você escolheu falar com um atendente. "
            "Aguarde na linha, estamos conectando você a um dos nossos especialistas. "
            "Isso pode levar alguns instantes."
            "Fim da simulação, retornando para o menu principal."
        ),

        "resposta_sair": (
            "Encerrando o atendimento. "
            "Obrigado por utilizar o serviço de voz da QuantumFinance. "
            "Tenha um ótimo dia, Jefferson!"

        ),
        
        "nao_identificado": (
            "Desculpe, não consegui entender sua escolha. "
            "Por favor, repita a opção desejada:"
        )
    }

def garantir_audios_fixos(msgs: dict[str, str]) -> dict[str, str]:
    """
    Gera os mp3 das mensagens fixas se não existirem.
    Retorna um dict com caminhos de arquivo.
    """
    caminhos = {}
    garantir_pasta(AUDIO_DIR)
    for nome, texto in msgs.items():
        mp3_path = os.path.join(AUDIO_DIR, f"{nome}.mp3")
        if not os.path.exists(mp3_path):
            logging.info(f"[SETUP] Gerando áudio fixo: {nome}")
            gerar_audio(texto, mp3_path)
        else:
            logging.info(f"[SETUP] Áudio já existe: {mp3_path}")
        caminhos[nome] = mp3_path
    return caminhos

def loop_atendimento(caminhos: dict[str, str]):
    """
    1) Toca saudação + opções
    2) Escuta usuário (STT)
    3) Detecta opção por palavra-chave
    4) Responde e repete até 'sair'
    """
    # Saudação inicial + menu
    tocar_audio(caminhos["saudacao"])
    tocar_audio(caminhos["opcoes"])

    while True:
        texto_usuario = transcrever_audio(timeout=5, phrase_time_limit=5)

        if not texto_usuario:
            # Sem transcrição ou incompreensível
            tocar_audio(caminhos["nao_identificado"])
            tocar_audio(caminhos["opcoes"])
            continue

        opc = detectar_opcao(texto_usuario)
        logging.info(f"[LOGICA] Opção detectada: {opc}")

        if opc == "saldo":
            tocar_audio(caminhos["resposta_saldo"])
            tocar_audio(caminhos["opcoes"])
        elif opc == "compra":
            tocar_audio(caminhos["resposta_compra"])
            tocar_audio(caminhos["opcoes"])
        elif opc == "atendente":
            tocar_audio(caminhos["resposta_atendente"])
            tocar_audio(caminhos["opcoes"])
        elif opc == "sair":
            tocar_audio(caminhos["resposta_sair"])
            break
        else:
            tocar_audio(caminhos["nao_identificado"])
            tocar_audio(caminhos["opcoes"])

def main():
    setup_logs()
    logging.info("=== QuantumFinance Voice Bot iniciado ===")

    msgs = preparar_mensagens()
    caminhos = garantir_audios_fixos(msgs)

    try:
        loop_atendimento(caminhos)
    except KeyboardInterrupt:
        logging.info("Interrompido pelo usuário (CTRL+C).")
    finally:
        logging.info("=== QuantumFinance Voice Bot finalizado ===")

if __name__ == "__main__":
    main()
