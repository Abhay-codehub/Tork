import datetime
import shutil
import wikipedia
import webbrowser
import speech_recognition as sr
import pyttsx3
import os


engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
#print(voices[0].id)
engine.setProperty('voice',voices[0].id)

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
 print("Welcome Mr.",uname.center(columns))
 speak("How can I hElp You, Sir")


def takeCommand():
    #It takes microphone input and return string output
    r = sr.Recognizer()
    with sr.Microphone() as source:
       print("Listening.....")
       r.pause_threshold = 1

       r.dynamic_energy_threshold = True
       audio = r.listen(source)
    try:
         print("Recognizing....")
         query = r.recognize_google(audio,language = 'en-in')
         print(f"User said  {query}\n")
    except Exception as e:
        #print(e)
        print("Say that again please")
        return "None"
    return query




if __name__ == '__main__':

    speak(" Hello, I Am Jarvis . Please tell me,How can i Help you?")
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

        elif 'open google' in query:
           speak("Opening Chrome with user id")
           webbrowser.open("google.com")

        elif 'open stackoverflow' in query:
            speak("Opening Stackoverflow")
            webbrowser.open("stackoverflow.com")

        elif 'play music' in query:
            music_dir = 'spotify'
            songs = os.listdir(music_dir)
            print(songs)
            os.startfile((os.path.join(music_dir,songs[0])))

        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"Sir, the time is {strTime}")

        elif 'send email to yash' in query:
            try:
                speak("What Should i Send")
                content = takeCommand()
                to = "yashtandonyouremail@gmail.com"
                sendEmail(to,content)
                speak("Email has Been Sent")
            except Exception as e:
                print(e)
                speak("Sorry my friend email has not been sent")


        elif 'send a mail' in query:
            try:
                speak("What should I say?")
                content = takeCommand()
                speak("whom should i send")
                to = input()
                sendEmail(to, content)
                speak("Email has been sent !")
            except Exception as e:
                print(e)
                speak("I am not able to send this email")


        elif 'how are you' in query:
            speak(" I Am Fine,Thank you")
            speak("How are You,Sir")

        elif 'fine' in query or'good' in query:
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

