import numpy as np
import streamlit as st
import pyaudio, openai
import wave
import tempfile
from openai import OpenAI
from pydub import AudioSegment
from app import process_audio


# Function to record audio
def record_audio(duration:int, filename_wav):
    chunk = 1024
    sample_format = pyaudio.paInt16
    channels = 2
    fs = 44100
    p = pyaudio.PyAudio()

    stream = p.open(format=sample_format,
                    channels=channels,
                    rate=fs,
                    frames_per_buffer=chunk,
                    input=True)

    frames = []

    # Store data in chunks for the duration of the recording
    for _ in range(0, int(fs / chunk * duration)):
        data = stream.read(chunk)
        frames.append(data)

    # Stop and close the stream
    stream.stop_stream()
    stream.close()
    p.terminate()

    # Save the recorded data as a WAV file
    wf = wave.open(filename_wav, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(sample_format))
    wf.setframerate(fs)
    wf.writeframes(b''.join(frames))
    wf.close()


# Streamlit app
col1, col2 = st.columns([2, 1])

# Column 1: Title and Subheader with Markdown for better formatting
with col1:
    st.markdown("<h1 style='text-align: center; color: black;'>PrescribeAI</h1>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center; color: gray;'>Get AI Based Prescription!</h2>", unsafe_allow_html=True)

# Column 2: Image
with col2:
    st.image("Images/reports.png", caption="AI-powered Medical Assistance", use_column_width=True)

# Add some spacing
st.write("### Start Recording Your Conversation!")
duration = st.slider("Select recording duration (seconds)", 1, 1800, 10)

if st.button("Record"):
    with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as tmpfile_wav:
        record_audio(duration, tmpfile_wav.name)

        # Convert WAV to MP3
        audio = AudioSegment.from_wav(tmpfile_wav.name)
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as tmpfile_mp3:
            audio.export(tmpfile_mp3.name, format="mp3")
            st.audio(tmpfile_mp3.name, format='audio/mp3')

            # Call the backend processing function
            st.write("AI Response:")
            st.write(process_audio(tmpfile_mp3.name))
