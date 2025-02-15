import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import requests
from openai import OpenAI
from gtts import gTTS
import pygame
import os
import time
import pyjokes

# pip install pocketsphinx

recognizer = sr.Recognizer()
engine = pyttsx3.init() 
newsapi = '84bc1accb3e1405a94db809e616fe426'

def speak_old(text):
    engine.say(text)
    engine.runAndWait()

def speak(text):
    tts = gTTS(text)
    tts.save('hello.mp3') 

    # Initialize Pygame mixer
    pygame.mixer.init()

    # Load the MP3 file
    pygame.mixer.music.load('hello.mp3')

    # Play the MP3 file
    pygame.mixer.music.play()

    # Keep the program running until the music stops playing
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    
    pygame.mixer.music.unload()
    os.remove("hello.mp3") 


def aiProcess(command):
    client = OpenAI(api_key="sk-1234abcd5678efgh1234abcd5678efgh1234abcd",
    )

    completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a virtual assistant named jarvis skilled in general tasks like Alexa and Google Cloud. Give short responses please"},
        {"role": "user", "content": command}
    ]
    )

    return completion.choices[0].message.content


def open_software(command):
    apps = {
        "notepad": "notepad.exe",
        "calculator": "calc.exe",
        "chrome": r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        "vlc": r"C:\Program Files\VideoLAN\VLC\vlc.exe",
        "word": r"C:\Program Files\Microsoft Office\root\Office16\WINWORD.EXE",
        #"spotify": r"C:\Program Files\WindowsApps\SpotifyAB.SpotifyMusic_1.256.502.0_x64__zpdnekdrzrea0\Spotify.exe"
    }

    words = command.lower().split()  # Split command into words

    for word in words:
        if word in apps:  # Check if any word matches an app
            speak(f"Opening {word}")
            try:
                os.startfile(apps[word])
                return
            except FileNotFoundError:
                speak(f"Sorry, {word} is not installed.")

         # Handle Spotify separately
        if word == "spotify":
            speak("Opening Spotify")
            os.system("start shell:AppsFolder\\SpotifyAB.SpotifyMusic_zpdnekdrzrea0!Spotify")
            return
        

    speak("Sorry, I don't recognize that command.")


def processCommand(c):
    responses = {
        "How are u": "I'm good, Sumit! Thanks for asking.",
        "what is your name": "My name is Jenny, your personal assistant!",
        "who created you": "I was created by Sumit Toshniwal.",
        "what is the time": "The current time is " + time.strftime("%I:%M %p"),
        "what is the date": "Today's date is " + time.strftime("%B %d, %Y"),
        "Who are u": "I am Jenny, your virtual assistant!",
        "tell me a joke": pyjokes.get_joke(),
        "propose me": "will u be my husband"
    }

    c = c.lower()  # Convert to lowercase for better matching

    if c in responses:
        speak(responses[c])  # Speak the predefined response
    elif "time" in c:
        speak("The current time is " + time.strftime("%I:%M %p"))
    elif "date" in c:
        speak("Today's date is " + time.strftime("%B %d, %Y"))

    elif "open google" in c.lower():
        speak("Opening Google")
        webbrowser.open("https://google.com")

    elif "open facebook" in c.lower():
        webbrowser.open("https://facebook.com")

    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")

    elif "open linkedin" in c.lower():
        webbrowser.open("https://linkedin.com")

    elif c.lower().startswith("play"):
        song = c.lower().split(" ")[1]
        link = musicLibrary.music[song]
        webbrowser.open(link)

    elif "news" in c.lower(): 
      url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={newsapi}"
      r = requests.get(url)
    
      print(r.status_code, r.text)  # Debugging step
    
      if r.status_code == 200:
        data = r.json()
        articles = data.get('articles', [])

        if not articles:
            speak("Sorry, I couldn't find any news right now.")
            return

        for article in articles[:5]:  # Limit to 5 headlines
            speak(article['title'])
      else:
        speak("Sorry, I couldn't fetch the news.")


    elif "open" in c.lower():
        open_software(c)

    else:
        # Let OpenAI handle the request
        output = aiProcess(c)
        speak(output) 




if __name__ == "__main__":
    speak("Jenny is Here....")
    while True:
        # Listen for the wake word "Jarvis"
        # obtain audio from the microphone
        r = sr.Recognizer()
         
        print("recognizing...")
        try:
            with sr.Microphone() as source:
                print("Listening...")
                audio = r.listen(source, timeout=2, phrase_time_limit=2)
            word = r.recognize_google(audio)
            if(word.lower() == "jenny" or "hloo" or "suno" or "hyy jenny"):
                speak("Yes Sumiiiii")
                # Listen for command
                with sr.Microphone() as source:
                    print("Jenny Active...")
                    audio = r.listen(source)
                    command = r.recognize_google(audio)

                    processCommand(command)


        except Exception as e:
            print("Error; {0}".format(e))