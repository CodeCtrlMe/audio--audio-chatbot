import speech_recognition as sr
import wikipedia
import pyttsx3

def speak(text):
    engine = pyttsx3.init()
    engine.setProperty("rate", 170)
    engine.say(text)
    engine.runAndWait()
    engine.stop()

def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.adjust_for_ambient_noise(source, duration=0.5)
        audio = r.listen(source)

    try:
        text = r.recognize_google(audio)
        print("You said:", text)
        return text.lower()
    except sr.UnknownValueError:
        speak("Sorry, I did not understand.")
        return ""
    except sr.RequestError:
        speak("Speech recognition error.")
        return ""

def get_answer(query):
    try:
        wikipedia.set_lang("en")
        return wikipedia.summary(query, sentences=2)
    except wikipedia.exceptions.DisambiguationError:
        return "Your question is too broad. Please be more specific."
    except wikipedia.exceptions.PageError:
        return "I could not find information on that."
    except Exception:
        return "Something went wrong."

def main():
    speak("Live audio to audio chatbot started. Ask me a question.")

    while True:
        query = listen()

        if query == "":
            continue

        if "exit" in query or "stop" in query or "quit" in query:
            speak("Goodbye. Have a nice day.")
            break

        answer = get_answer(query)
        print("Bot:", answer)
        speak(answer)

if __name__ == "__main__":
    main()