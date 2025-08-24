# QuantumFinance Voice Bot

## Visão Geral

Este projeto faz parte do MBA e tem como objetivo implementar um
protótipo de atendimento por voz para a empresa fictícia
**QuantumFinance**.\
O sistema permite que um cliente interaja com a aplicação por **voz**,
utilizando tecnologias de **Text-to-Speech (TTS)** e **Speech-to-Text
(STT)**.

## Funcionalidades

-   **Saudação inicial** e apresentação das opções.
-   **Opções disponíveis**:
    1.  Consulta ao saldo da conta.
    2.  Simulação de compra internacional.
    3.  Falar com um atendente.
    4.  Sair do atendimento.
-   **Confirmação por voz** para cada opção selecionada.
-   **Mensagem de erro** caso nenhuma opção seja identificada.
-   **Loop de atendimento**, encerrado apenas quando o cliente escolhe
    "Sair".
-   **Reconhecimento de voz por palavras-chave**, não apenas números.

## Tecnologias Utilizadas

-   **Python 3.12**
-   **Bibliotecas principais**:
    -   `gTTS` para geração de áudios (TTS)
    -   `SpeechRecognition` com fallback `sounddevice` (STT)
    -   `pygame` para reprodução dos áudios
    -   `pydub` para manipulação de áudio
    -   `Unidecode` para normalização de texto
-   **Plataforma**: execução local com ambiente virtual (`venv`).

## Estrutura do Projeto

    voice_app/
    │── app.py            # Orquestra o atendimento por voz
    │── tts.py            # Funções de geração de áudio (TTS)
    │── stt.py            # Funções de transcrição (STT)
    │── player.py         # Funções para reproduzir áudios
    │── utils.py          # Funções auxiliares (logs, normalização)
    │── audios/           # Áudios pré-gerados
    │── requirements.txt  # Dependências do projeto

## Instalação e Execução

1.  **Criar ambiente virtual**:

    ``` bash
    python3 -m venv .venv
    source .venv/bin/activate    # Linux/Mac
    .venv\Scripts\activate       # Windows
    ```

2.  **Instalar dependências**:

    ``` bash
    pip install -r requirements.txt
    ```

3.  **Executar o aplicativo**:

    ``` bash
    python app.py
    ```

4.  **Encerrar**: pressione `CTRL + C` ou escolha a opção "Sair do
    atendimento".

## Observações Importantes

-   Em sistemas macOS com arquitetura **x86_64**, pode haver
    incompatibilidade com o PyAudio. Este projeto já possui **fallback
    com sounddevice**, que grava o áudio por janelas e envia para a API
    do Google Speech Recognition.
-   Ajuste as palavras-chave em `utils.py` conforme necessário para
    maior precisão no reconhecimento.

## Autores

-   Jefferson de Souza Santos (projeto individual para disciplina de
    **Audio Recognition**)
