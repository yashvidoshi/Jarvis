import pyttsx3
import platform
import datetime
import wikipedia
import webbrowser
import pywhatkit
import subprocess
import speech_recognition as sr
from groq import Groq
import os

# Optional FLAC converter for macOS
sr.AudioFile.FLAC_converter = "/opt/homebrew/bin/flac"

# Initialize voice engine
system = platform.system()
if system == 'Windows':
    engine = pyttsx3.init('sapi5')
elif system == 'Darwin':
    engine = pyttsx3.init('nsss')
else:
    engine = pyttsx3.init()

voices = engine.getProperty('voices')
engine.setProperty('voice', voices[4].id)  # Use voices[14] if available

def speak(audio):
    # print("Jarvis:", audio)
    engine.say(audio)
    engine.runAndWait()

def wishme():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good Morning!")
    elif hour >= 12 and hour < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")
    speak("I am Jarvis. How may I help you?")

def takecommand():
    r = sr.Recognizer()
    mic_index = 0  # Change this index as needed

    with sr.Microphone(device_index=mic_index) as source:
        print("Listening...")
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
    except Exception as e:
        print(f"Error: {e}")
        return "none"

    return query.lower()

# Groq LLaMA 3 AI integration
def ask_groq(query):
    client = Groq(api_key="_____________________")  #Replace with your real key

    try:
        response = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[
                {"role": "system", "content": "You are Jarvis, a helpful AI assistant."},
                {"role": "user", "content": query}
            ],
            temperature=0.3
        )
        answer = response.choices[0].message.content
        speak(answer)
    except Exception as e:
        print("Groq API error:", e)
        speak("Sorry, I couldn't get an answer from AI.")

# Map for opening local applications
app_map = {
    "chrome": "Google Chrome",
    "spotify": "Spotify",
    "safari": "Safari",
    "notes": "Notes",
    "code": "Visual Studio Code",
    "vs code": "Visual Studio Code",
    "terminal": "Terminal"
}

# Start assistant
wishme()

while True:
    query = takecommand()

    if query in ["none", ""]:
        continue

    elif 'wikipedia' in query:
        speak("Searching Wikipedia...")
        query = query.replace("wikipedia", "")
        try:
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia:")
            print(results)
            speak(results)
        except Exception as e:
            print(e)
            speak("Sorry, I couldn't find anything on Wikipedia.")

    elif 'open youtube' in query:
        speak("Opening YouTube...")
        webbrowser.open("https://www.youtube.com")

    elif 'open google' in query:
        speak("Opening Google...")
        webbrowser.open("https://www.google.com")

    elif 'play' in query:
        song = query.replace("play", "").strip()
        speak(f"Playing {song} on YouTube...")
        pywhatkit.playonyt(song)

    elif 'time' in query:
        strTime = datetime.datetime.now().strftime("%H:%M:%S")
        speak(f"The time is {strTime}")

    elif 'open' in query:
        spoken = query.replace("open", "").strip().lower()
        app_name = app_map.get(spoken, spoken.title())

        try:
            speak(f"Opening {app_name}...")
            subprocess.Popen(["open", "-a", app_name])
        except Exception as e:
            speak(f"Sorry, I couldn't open {app_name}.")
            print(e)

    elif query in ['exit', 'stop', 'quit', 'bye']:
        speak("Goodbye! Have a great day.")
        break

    else:
        ask_groq(query)
