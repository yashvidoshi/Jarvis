import pyttsx3
import platform
import datetime
import wikipedia
import webbrowser
import pywhatkit
import subprocess
import speech_recognition as sr
import os

sr.AudioFile.FLAC_converter = "/opt/homebrew/bin/flac"

# for index, name in enumerate(sr.Microphone.list_microphone_names()):
    # print(f"Microphone with index {index}: {name}")

system = platform.system()

if system == 'Windows':
    engine = pyttsx3.init('sapi5')
elif system == 'Darwin':  # macOS
    engine = pyttsx3.init('nsss')
else:
    engine = pyttsx3.init()  # fallback (works on many Linux distros)

voices = engine.getProperty('voices')
engine.setProperty('voice', voices[14].id)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def wishme():
    hour= int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        speak("Good Morning!")
    elif hour>=12 and hour<18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")

    speak("I am Jarvis. How may I help you?")

def takecommand():
    r = sr.Recognizer()
    mic_index = 0  # Replace 0 with the correct index from your list

    with sr.Microphone(device_index=mic_index) as source:
        print("Listening through correct mic...")
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
    except Exception as e:
        print(f"Error: {e}")
        return "none"

    return query

app_map = {

        "chrome": "Google Chrome",
        "spotify": "Spotify",
        "safari": "Safari",
        "notes": "Notes",
        "code": "Visual Studio Code",
        "vs code": "Visual Studio Code",
        "terminal": "Terminal"
}

wishme()

while True:
    query=takecommand().lower()

    if 'wikipedia' in query:
        speak("Searching Wikipeda...")
        query=query.replace("wikipedia", "")
        results=wikipedia.summary(query,sentences=2)
        speak("According to Wikipedia")
        print(results)
        speak(results)

    elif 'open youtube' in query:
        speak("Opening YouTube...")
        webbrowser.open("https://www.youtube.com")

    elif 'open google' in query:
        speak("Opening Google...")
        webbrowser.open("https://www.google.com/?client=safari")

    elif 'play' in query:
        song = query.replace("play", "").strip()
        speak(f"Playing {song} on YouTube...")
        pywhatkit.playonyt(song)

    elif 'time' in query:
        strTime=datetime.datetime.now().strftime("%H:%M:%S")
        speak(f"This time is {strTime}")

    elif 'open' in query:
        spoken = query.replace("open", "").strip().lower()
        app_name = app_map.get(spoken, spoken.title())

        try:
            speak(f"Opening {app_name}...")
            print(f'Command: open -a "{app_name}"')
            subprocess.Popen(["open", "-a", app_name])


        except Exception as e:
            speak(f"Sorry, I couldn't open {app_name}.")
            print(e)
    
