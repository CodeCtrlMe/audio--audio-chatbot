import streamlit as st
import speech_recognition as sr
import wikipedia
from gtts import gTTS
import tempfile
import os

st.set_page_config(page_title="Audio-to-Audio Chatbot", layout="centered")

st.title("🎤 Audio-to-Audio Chatbot")
st.write("Speak a question. The bot will answer using Wikipedia and speak back.")

recognizer = sr.Recognizer()

audio_file = st.audio_input("Click and speak")

if audio_file is not None:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        tmp.write(audio_file.getvalue())
        audio_path = tmp.name

    with sr.AudioFile(audio_path) as source:
        audio_data = recognizer.record(source)

    try:
        user_text = recognizer.recognize_google(audio_data)
        st.success(f"You said: {user_text}")

        wikipedia.set_lang("en")
        answer = wikipedia.summary(user_text, sentences=3)
        st.info(answer)

        tts = gTTS(answer)
        tts_path = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3").name
        tts.save(tts_path)

        st.audio(tts_path, format="audio/mp3")

    except wikipedia.exceptions.DisambiguationError:
        st.error("Your question is too broad. Please be more specific.")

    except wikipedia.exceptions.PageError:
        st.error("No Wikipedia page found.")

    except Exception as e:
        st.error("Sorry, I could not understand the audio.")

    finally:
        os.remove(audio_path)
