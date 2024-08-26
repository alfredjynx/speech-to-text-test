import streamlit as st
from audio_conversion import *
import speech_recognition as sr

def st_speech():
    st.title("Speech Recognition MASP Test")

    file_load_state = st.text('Procurando Áudio...\nPor Favor Colocar Link Para Áudio')

    file_path = ""
    
    met = st.sidebar.selectbox(
        'Qual é o método?',
        ('Live Capture', 'File Path')
    )
    
    
    if met == 'File Path':

        file_path = st.sidebar.text_input(
            "Coloque o File Path do áudio aqui! 👇"
        )

        if file_path:
            st.write("\n\nYou entered: ", file_path)




    algorithm = st.sidebar.selectbox(
        'Qual é o idioma?',
        ('Português', 'English')
    )


    if algorithm == 'English':
        language = 'en'
    else:
        language = "pt-BR"




    if st.sidebar.button("Transcrever Áudio"):
        if met == 'Live Capture':
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
                frase = microfone.recognize_google(audio, language='pt-BR')
                # Após alguns segundos, retorna a frase falada
                st.write("Você disse: " + frase)
            # Caso não tenha reconhecido o padrão de fala, exibe esta mensagem
            except sr.UnknownValueError:
                st.write("Não entendi")
            except sr.RequestError:
                st.write("Não foi possível se conectar ao serviço de reconhecimento de fala.")
        else:
            st.write("O áudio diz: " + transcribe_audio(file_path, language))
            
st_speech()