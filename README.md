# QuantumFinance Voice Bot

## Visão Geral

Este projeto faz parte do MBA e tem como objetivo implementar um
protótipo de atendimento por voz para a empresa fictícia
**QuantumFinance**.\
O sistema permite que um cliente interaja com a aplicação por **voz**,
utilizando tecnologias de **Text-to-Speech (TTS)** e **Speech-to-Text
(STT)**, e agora também conta com uma **interface web interativa via
Streamlit**.

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
-   **Aplicativo Streamlit** para iniciar e controlar a simulação:
    -   Botão para **iniciar a simulação** (executa o `app.py`).
    -   Botão para **encerrar a simulação**.
    -   Painel com **logs em tempo real** (o log é limpo a cada início).

## Tecnologias Utilizadas

-   **Python 3.12**
-   **Bibliotecas principais**:
    -   `gTTS` para geração de áudios (TTS)
    -   `SpeechRecognition` com fallback `sounddevice` (STT)
    -   `pygame` para reprodução dos áudios
    -   `pydub` para manipulação de áudio
    -   `Unidecode` para normalização de texto
    -   `Streamlit` para interface web
-   **Plataforma**: execução local com ambiente virtual (`venv`).

## Estrutura do Projeto

    voice_app/
    │── app.py               # Orquestra o atendimento por voz
    │── tts.py               # Funções de geração de áudio (TTS)
    │── stt.py               # Funções de transcrição (STT)
    │── player.py            # Funções para reproduzir áudios
    │── utils.py             # Funções auxiliares (logs, normalização)
    │── app_streamlit.py     # Interface web para iniciar/encerrar simulação e visualizar logs
    │── audios/              # Áudios pré-gerados
    │── quantumvoice.log     # Arquivo de log (limpo a cada execução no Streamlit)
    │── requirements.txt     # Dependências do projeto

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

3.  **Executar o aplicativo de voz (terminal)**:

    ``` bash
    python app.py
    ```

4.  **Executar a interface web (Streamlit)**:

    ``` bash
    streamlit run app_streamlit.py
    ```

5.  **Controle pelo Streamlit**:

    -   Clique **Iniciar simulação** para rodar o `app.py`.
    -   Use **Encerrar simulação** para parar.
    -   O **log** é limpo automaticamente a cada início e exibido no
        painel.
    -   O áudio toca pelo sistema local, e a fala é capturada pelo
        microfone local.

## Observações Importantes

-   Em sistemas macOS com arquitetura **x86_64**, pode haver
    incompatibilidade com o PyAudio. Este projeto já possui **fallback
    com sounddevice**, que grava o áudio por janelas e envia para a API
    do Google Speech Recognition.
-   Ajuste as palavras-chave em `utils.py` conforme necessário para
    maior precisão no reconhecimento.
-   O Streamlit **não transmite áudio pelo navegador**: ele apenas
    controla o app que roda localmente.

## Autores

-   Jefferson de Souza Santos (projeto individual para disciplina de
    **Audio Recognition**)
