import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import os
import smtplib
import urllib.request
import urllib.parse
import re

print("Initializing Jarvis")

MASTER = "Tri"
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)


#speak functiun will pronouce string which is passed to it
def speak(text):
    engine.say(text)
    engine.runAndWait()

#this function will speak wish you as per the current time
def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good Morning" + MASTER)
    elif hour >= 12 and hour < 18:
        speak("Good Afternoon" + MASTER)
    else:
        speak("Good Evening" + MASTER)
    speak("I am Jarvis. How may I help you ?")

#this function will take command from your microphone
def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening....")
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
        
    try:
        query = r.recognize_google(audio).lower()
        print("You said: ", query)
    except sr.UnknownValueError:
        # speech was unintelligible
        query = None
        print('Unable to recognize speech')
    except sr.RequestError:
        # API was unreachable or unresponsive
        query = None
        print('Google API was unreachable')
    return query

#this function help you to send email
def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('youremail@gmail.com', 'password')
    server.sendmail("yourfriendemail@gmail.com", to, content)
    server.close()

#this function help you check when you say goodbye
def checkgoodbye(query):
    if 'goodbye Jarvis' in query.lower():
        quit()
    print(f"Goodbye {MASTER}")
    
#Main progaram
def main():
    
    query = takeCommand()

    #logic for executing tasks as per the query
    if 'wikipedia' in query.lower():
        speak('Searching wikipedia...')
        query = query.replace("wikipedia","")
        results = wikipedia.summary(query, sentences = 5)
        print(results)
        speak(results)

    elif 'open youtube' in query.lower():
        url = 'youtube.com'
        chrome_path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'
        webbrowser.get(chrome_path).open(url)
        
    elif 'open google' in query.lower():
        url = 'google.com'
        chrome_path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'
        webbrowser.get(chrome_path).open(url)
        
    elif 'open facebook' in query.lower():
        url = 'facebook.com'
        chrome_path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'
        webbrowser.get(chrome_path).open(url)
        
    elif 'play music' in query.lower():
        speak("Please type your song")
        query_string = urllib.parse.urlencode({"The song you want to play : " : input()})
        html_content = urllib.request.urlopen("http://www.youtube.com/results?"+query_string)
        search_results = re.findall(r'href=\"\/watch\?v=(.{11})', html_content.read().decode())
        print("http://www.youtube.com/watch?v=" + search_results[0])
        url = "http://www.youtube.com/watch?v={}".format(search_results[0])
        chrome_path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'
        webbrowser.get(chrome_path).open(url)
        
    elif 'the time' in query.lower():
        strTime = datetime.datetime.now().strftime("%H:%M:%S")
        speak(f"{MASTER} the time is {strTime}")
        
    elif 'open code' in query.lower():
        codePath = "C:\\Users\\XV\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
        os.startfile(codePath)

    elif 'email to friend' in query.lower():
        try:
            speak("What should I send")
            content = takeCommand()
            to = "yourfriendemail@gmail.com"
            sendEmail(to, content)
            speak("Email has been sent sucessfully")
        except Exception as e:
            print(e)
 
 
            
speak(f"hello {MASTER}")
wishMe()
while (True):
    query = takeCommand()
    main()
    checkgoodbye(query)


 