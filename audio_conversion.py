import os
from dotenv import load_dotenv
import streamlit as st

from deepgram import (
    DeepgramClient,
    PrerecordedOptions,
)

load_dotenv()


API_KEY = os.getenv("DG_API_KEY")


def convert_deepgram(url, language):
    try:
        # STEP 1 Create a Deepgram client using the API key
        deepgram = DeepgramClient(API_KEY)

        #STEP 2: Configure Deepgram options for audio analysis
        options: PrerecordedOptions = PrerecordedOptions(
            language=language,
            # language="en",
            model="nova-2",
            smart_format=True,
        )
        
        audio = {
           'url': url
        }

        # STEP 3: Call the transcribe_url method with the audio payload and options
        response = deepgram.listen.prerecorded.v("1").transcribe_url(audio, options)

        # STEP 4: Print the response
        print(response.to_json(indent=4))
        
        return response.results.channels[0].alternatives[0]['transcript']

    except Exception as e:
        print(f"Exception: {e}")
        raise e
    
    
    
    
import speech_recognition as sr

# importing libraries 
import speech_recognition as sr 
import os 
from pydub import AudioSegment
from pydub.silence import split_on_silence

# create a speech recognition object
r = sr.Recognizer()

# a function to recognize speech in the audio file
# so that we don't repeat ourselves in in other functions
def transcribe_audio(path, language):
    # use the audio file as the audio source
    with sr.AudioFile(path) as source:
        audio_listened = r.record(source)
        # try converting it to text
        text = r.recognize_google(audio_listened, language = language)
    return text

# a function that splits the audio file into chunks on silence
# and applies speech recognition
def get_large_audio_transcription_on_silence(path, language):
    """Splitting the large audio file into chunks
    and apply speech recognition on each of these chunks"""
    # open the audio file using pydub
    sound = AudioSegment.from_file(path)  
    # split audio sound where silence is 500 miliseconds or more and get chunks
    chunks = split_on_silence(sound,
        # experiment with this value for your target audio file
        min_silence_len = 500,
        # adjust this per requirement
        silence_thresh = sound.dBFS-14,
        # keep the silence for 1 second, adjustable as well
        keep_silence=500,
    )
    folder_name = "audio-chunks"
    # create a directory to store the audio chunks
    if not os.path.isdir(folder_name):
        os.mkdir(folder_name)
    whole_text = ""
    # process each chunk 
    for i, audio_chunk in enumerate(chunks, start=1):
        # export audio chunk and save it in
        # the `folder_name` directory.
        chunk_filename = os.path.join(folder_name, path.split("/")[-1]+f"_chunk{i}.wav")
        audio_chunk.export(chunk_filename, format="wav")
        # recognize the chunk
        try:
            text = transcribe_audio(chunk_filename, language)
        except sr.UnknownValueError as e:
            st.write("Error:", str(e))
        else:
            text = f"{text.capitalize()}. "
            st.write("-"*50)
            st.write(chunk_filename, ":", text)
            whole_text += text
    # return the text for all chunks detected
    st.write("-"*50)
    return whole_text
