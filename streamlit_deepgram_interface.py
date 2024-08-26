import streamlit as st
from audio_conversion import convert_deepgram

def st_deepgram():
    st.title("Deepgram MASP Test")

    file_load_state = st.text('Procurando Áudio...\nPor Favor Colocar Link Para Áudio')

    file_path = ""

    file_path = st.sidebar.text_input(
        "Coloque a URL do áudio aqui! 👇"
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
        try:
            text = convert_deepgram(url=file_path, language=language)
            file_load_state.text(text)
        except Exception as e:
            file_load_state.text(e)
            
st_deepgram()