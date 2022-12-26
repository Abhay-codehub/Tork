import ctypes
import datetime
import shutil
import ecapture as ec
import winshell as winshell
import wolframalpha
import pyjokes as pyjokes
import wikipedia
import webbrowser
import speech_recognition as sr
import pyttsx3
import os
import smtplib
import subprocess
import time

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
# print(voices[0].id)
engine.setProperty('voice', voices[0].id)


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def username():
    speak("What should I call you sir")
    uname = takeCommand()
    speak("Welcome Mister")
    speak(uname)
    columns = shutil.get_terminal_size().columns
    print("####################".center(columns))
    print("Welcome Mr.", uname.center(columns))
    speak("How can I hElp You, Sir")


def takeCommand():
    # It takes microphone input and return string output
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening.....")
        r.pause_threshold = 1
        r.energy_threshold = 150

        r.dynamic_energy_threshold = True
        audio = r.listen(source)
    try:
        print("Recognizing....")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said  {query}\n")
    except Exception as e:
        # print(e)
        print("Say that again please")
        return "None"
    return query


if __name__ == '__main__':
    speak(" Hello, I Am Jarvis Sir . Please tell me,How can i Help you?")
    username()
while True:
    # if 1:
    query = takeCommand().lower()

    # Logic for executing tasks based on query
    if 'wikipedia' in query:
        speak('Searching Wikipedia...')
        query = query.replace("wikipedia", "")
        results = wikipedia.summary(query, sentences=2)
        speak("According to Wikipedia")
        print(results)
        speak(results)

    elif 'open youtube' in query:
        speak('Opening Youtube...')
        webbrowser.open("youtube.com")

    elif 'open google' in query or 'open chrome' in query:
        speak("Opening Chrome with user id")
        webbrowser.open("google.com")

    elif 'open new tab in google' in query or 'new tab' in query:
        speak("Opening the new Tab")
        webbrowser.open_new_tab("google.com")




    elif 'open stackoverflow' in query:
        speak("Opening Stackoverflow")
        webbrowser.open("stackoverflow.com")

    elif 'play music' in query:
        music_dir = 'spotify'
        songs = os.listdir(music_dir)
        print(songs)
        os.startfile((os.path.join(music_dir, songs[0])))

    elif 'the time' in query:
        strTime = datetime.datetime.now().strftime("%H:%M:%S")
        speak(f"Sir, the time is {strTime}")




    elif 'how are you' in query:
        speak(" I Am Fine,Thank you")
        speak("How are You,Sir")

    elif 'fine' in query:
        speak("I am Happy to know that ")

    elif 'who made you' in query:
        speak(" I have been created by Yash Tandon")

    elif 'who are your friends' in query:
        speak("My Friends are Alexa and Siri")

    elif 'exit' in query or 'stop' in query:
        speak("Thanks for giving me your time,Sir")
        exit()
    elif 'what is your name' in query:
        speak("my Name is Jarvis")

    elif 'joke' in query:
        speak(pyjokes.get_joke())

    elif 'lock window' in query:
        speak('locking the device')
        ctypes.windll.user32.LockWorkStation()

    elif "change my name to" in query:
        speak("What would you like to call me,Sir")
        query = query.replace("change my name to", "")
        assname = query
        speak("That is a good one,Sir!")

    elif 'change name' in query:
        speak("What would you like to call me,Sir")
        assname = takeCommand()
        speak("My Friends Call me that")

    elif 'thank you' in query:
        speak("Always Available Sir,anytime")

    elif 'welcome' in query:
        speak("I think i should say that")

    elif 'Good Morning' in query:
        speak("Good Morning Sir, nice to hear from you")

    elif 'Good Afternoon' in query:
        speak("Good Afternoon Sir!")

    elif 'Good Evening' in query:
        speak("Good Evening Sir!")

    elif 'Good Night' in query:
        speak("Good Night Sir, to you too")

    elif 'who am i' in query:
        speak("If you can talk then definetly you are human")

    elif 'why you came to the world' in query:
        speak("Thanks to Yash. further It's a Secret")

    elif 'camera' in query or 'take a photo' in query:
        ec.capture(0, "Jarvis Camera", "img.jpg")

    elif 'help' in query:
        speak("What Should I Help you With Sir")
        help()

    elif "restart" in query:
        speak("Your Computer Will be Restarted Shortly,Sir")
        subprocess.call(["shutdown", "/r"])

    elif 'shutdown system' in query or 'jarvis close the system' in query:
        speak("Hold on a Second! Your System is on its way to shut down")
        subprocess.call(["shutdown", "/h"])

    elif 'open gmail' in query or 'please open my email' in query:
        speak("Ok, Mail will be opened in short span of time. Please Wait!")
        webbrowser.open("mail.google.com")

    elif 'open whatsapp' in query:
        speak("Opening Whatsapp, it will be opened shortly")
        webbrowser.open("web.whatsapp.com")

    elif 'open my contacts' in query or 'tell me the contact details of my account' in query:
        speak("Opening Contacts in chrome, please wait it will be opened shortly")
        webbrowser.open("contacts.google.com")

    elif 'what is my dowloading history' in query or 'what i have downloaded last from chrome' in query:
        speak("Opening Downloads in Chrome")
        webbrowser.open("chrome://downloads/")

    elif 'open settings' in query:
        speak("Opening Settings of Your Account in Chrome")
        webbrowser.open("chrome://settings/")

    elif 'open calender' in query or 'what is the date today' in query:
        speak("Opening Calender")
        webbrowser.open("calender.google.com")






