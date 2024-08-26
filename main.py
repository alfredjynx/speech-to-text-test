import streamlit as st
from streamlit_deepgram_interface import st_deepgram
from streamlit_speech_recognition_interface import st_speech
from audio_conversion import *

st.title("MASP Teste - Transcrição de Áudio")

file_path = ""

# Implementation selection
met = st.sidebar.selectbox(
    'Qual é a implementação?',
    ('Speech Recognition', 'Deepgram'),
    key="implementation"
)

if met == 'Speech Recognition':
    file_load_state = st.text('Procurando Áudio...\nPor Favor Colocar Link Para Áudio')

    file_path = ""

    # Method selection
    method = st.sidebar.selectbox(
        'Qual é o método?',
        ('Live Capture', 'File Path'),
        key="method"
    )
    
    size = "reg"

    if method == 'File Path':
        file_path = st.sidebar.text_input(
            "Coloque o File Path do áudio aqui! 👇",
            key="file_path"
        )

        if file_path:
            st.write("\n\nYou entered: ", file_path)
        
        file_size = st.sidebar.selectbox(
            'Qual é o tamanho do arquivo?',
            ('Regular', 'Grande'),
            key='speech_recognition_file_size'
        )
        
        if file_size == 'Grande':
            size = 'big'

    # Language selection
    language = st.sidebar.selectbox(
        'Qual é o idioma?',
        ('Português', 'English'),
        key='speech_recognition_language'
    )

    if language == 'English':
        language = 'en'
    else:
        language = "pt-BR"

    if st.sidebar.button("Transcrever Áudio", key="transcribe_speech_recognition"):
        if method == 'Live Capture':
            # Habilita o microfone para ouvir o usuário
            microfone = sr.Recognizer()
            with sr.Microphone() as source:
                # Chama a função de redução de ruído disponível no speech_recognition
                microfone.adjust_for_ambient_noise(source)
                # Avisa ao usuário que está pronto para ouvir
                st.write("Diga alguma coisa: ")
                # Armazena a informação de áudio na variável
                audio = microfone.listen(source)
                
            try:
                # Passa o áudio para o reconhecedor de padrões do speech_recognition
                frase = microfone.recognize_google(audio, language=language)
                # Após alguns segundos, retorna a frase falada
                st.write("Você disse: " + frase)
            # Caso não tenha reconhecido o padrão de fala, exibe esta mensagem
            except sr.UnknownValueError:
                st.write("Não entendi")
            except sr.RequestError:
                st.write("Não foi possível se conectar ao serviço de reconhecimento de fala.")
        else:
            if size == 'reg':
                st.write("O áudio diz: " + transcribe_audio(file_path, language))
            else:
                st.write("O áudio diz: " + get_large_audio_transcription_on_silence(file_path, language))
            
elif met == 'Deepgram':
    file_load_state = st.text('Procurando Áudio...\nPor Favor Colocar Link Para Áudio')

    file_path = st.sidebar.text_input(
        "Coloque a URL do áudio aqui! 👇",
        key="deepgram_file_path"
    )

    if file_path:
        st.write("\n\nYou entered: ", file_path)

    # Language selection for Deepgram
    algorithm = st.sidebar.selectbox(
        'Qual é o idioma?',
        ('Português', 'English'),
        key="deepgram_language"
    )

    if algorithm == 'English':
        language = 'en'
    else:
        language = "pt-BR"

    if st.sidebar.button("Transcrever Áudio", key="transcribe_deepgram"):
        try:
            text = convert_deepgram(url=file_path, language=language)
            file_load_state.text(text)
        except Exception as e:
            file_load_state.text(str(e))
