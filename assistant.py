from urllib import request
import pyttsx3
import datetime
import smtplib
from email.message import EmailMessage
import webbrowser as wb
from time import sleep
import pyautogui
import speech_recognition as sr
import wikipedia
from flask import Flask
import pywhatkit
import os
import requests
from newsapi import NewsApiClient
import pyjokes
import time as tt
from geopy.distance import great_circle
from geopy.geocoders import Nominatim
import geocoder
from bs4 import BeautifulSoup
import threading
import random
from nltk.tokenize import word_tokenize
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import QTimer,QTime,QDate,Qt
from PyQt5.QtGui import QMovie
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.uic import loadUiType
from assistantUi import Ui_MainWindow
import sys
import subprocess

engine = pyttsx3.init()

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def getvoices(voice):
    voices = engine.getProperty('voices')
    if voice==1:
        engine.setProperty('voice',voices[0].id)
        speak("Hello I'm at your Assistance")
    if voice==2:
        engine.setProperty('voice',voices[1].id)
        speak("Hello I'm at your Assistance")

def time():
    Time = datetime.datetime.now().strftime("%I:%M:%S")
    speak("The current time is:")
    speak(Time)

def date():
    year = int(datetime.datetime.now().year)
    month = int(datetime.datetime.now().month)
    day = int(datetime.datetime.now().day)
    speak("Today's date is")
    speak(day)
    speak(month)
    speak(year)

def greeting():
    hour=datetime.datetime.now().hour
    if hour>=6 and hour <12:
        speak("Good morning !")
    elif hour>=12 and hour<18:
        speak("Good Afternoon !")
    elif hour>=18 and hour<24:
        speak("Good evening !")
    else:
        speak("Welcome !")
def wishme():
    greeting()
    speak("How can I help you?")

def takeCommandCMD():
    query = input("How can I help You?")
    return query

  
def sendEmail(receiver, subject, content):
    server = smtplib.SMTP('smtp.gmail.com',587)
    server.starttls()
    server.login('assistant email goes here', 'assistant passwaord goes here') #server.login(senderemail, epwd)
    email=EmailMessage()
    email['From']='assistant email goes here' #email['From']=senderemail
    email['To']= receiver #email['To']= receiver
    email['Subject']= subject
    email.set_content(content)
    server.send_message(email)
    server.close()

def sendwhatsmsg(phone_no, message):
    Message = message
    wb.open('https://web.whatsapp.com/send?phone='+phone_no+'&text='+Message)
    sleep(20)

def searchgoogle(search):
    wb.open('https://www.google.com/search?q='+search)

def news(topic):
    newsapi=NewsApiClient(api_key='API key goes here')
    data= newsapi.get_top_headlines(q=topic,
                                    language='en',
                                    page_size=5)
    newsdata = data['articles']
    for x,y in enumerate(newsdata):
        print(f'{x}{y["description"]}')
        speak(f'{x}{y["description"]}')
    speak("That's the news update for now")

def open_camera():
    subprocess.run("start microsoft.windows.camera:", shell=True)

def ss():
    name_img= tt.time()
    name_img= 'path name goes here' #example: 'C:\\Users\\Shreya\\Desktop\\assistant\\Screenshots\\{name_img}.png'
    img= pyautogui.screenshot(name_img)
    img.show()

def GoogleMaps(Place):
    Url_Place = "https://www.google.com/maps/place/"+str(Place)
    geolocator=Nominatim(user_agent='myGeocoder')
    location=geolocator.geocode(Place,addressdetails=True)
    target_latlon=location.latitude , location.longitude
    location= location.raw['address']
    target={'city':location.get('city',''), 
            'state':location.get('state',''),
        'country':location.get('country','')}
    current_loca=geocoder.ip('me')
    current_latlon=current_loca.latlng
    distance=str(great_circle(current_latlon,target_latlon))
    distance=str(distance.split(' ',1)[0])
    distance=round(float(distance),2)
    wb.open(url=Url_Place)
    speak(target)
    speak(f'{Place} is {distance} kilometre away from your location')

def launch_app(path_of_app):
    try:
        subprocess.call([path_of_app])
        return True
    except Exception as e:
        print(e)
        return False  

def My_Location():
    ip_add = requests.get('https://api.ipify.org').text
    url='https://get.geojs.io/v1/ip/geo/'+ip_add+'.json'
    geo_q=requests.get(url)
    geo_d=geo_q.json()
    state=geo_d['city']
    country=geo_d['country']
    speak(f'You are now in {state,country}.')

class MainThread(QThread):
    def __init__(self):
        super(MainThread,self).__init__()

    def run(self):
        self.TaskExecution()

    def takeCommandMic(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening...")
            r.pause_threshold = 1
            audio = r.listen(source)
        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language="en-IN")
            print(query)
        except Exception as e:
            print(e)
            
            return "None"
        return query


    def TaskExecution(self):
        getvoices(1)
        wishme()
        wakeword='assistant'
        while True: 
            self.query = self.takeCommandMic().lower()
            self.query= word_tokenize(self.query)
            
            if wakeword in self.query:
                if 'time' in self.query:
                    time()
                elif 'date' in self.query:
                    date()
                elif 'email' in self.query:
                    email_list= {
                        'Name1 goes here': 'email1 goes here',
                        'Name2 goes here': 'email2 goes here' #,
                        # add more names and emails similarly
                    }
                    try:
                        speak("To whom?")
                        name = self.takeCommandMic()
                        receiver = email_list[name]
                        speak("What should be the subject of the mail?")
                        subject= self.takeCommandMic()
                        speak("What should I say?")
                        content = self.takeCommandMic()
                        sendEmail(receiver, subject, content)
                        speak("Email has been sent!")
                    except Exception as e:
                        print(e)
                        speak("Unable to send email")
                elif 'offline' in self.query:
                    speak("Bye bye")
                    quit()
                elif 'message' in self.query:
                    user_name = {
                        'Name1 goes here':'phone1 goes here',
                        'Name2 goes here': 'phone2 goes here' #,
                        # add more names and numbers similarly
                    }
                    try:
                        speak("To whom?")
                        name = self.takeCommandMic()
                        phone_no = user_name[name]
                        speak("What is the message?")
                        message= self.takeCommandMic()
                        sendwhatsmsg(phone_no, message)
                        speak("Message has been sent!")
                    except Exception as e:
                        print(e)
                        speak("Unable to send message")
                
                elif 'wikipedia' in self.query:
                    speak('Searching on wikipedia...')
                    #self.query = str(self.query).replace("wikipedia","")
                    self.query=self.query[-1]
                    result = wikipedia.summary(self.query,sentences=2)
                    print(result)
                    speak(result)
                
                elif 'search' in self.query:
                    speak('What should I search for?')
                    search = self.takeCommandMic()
                    searchgoogle(search)

                elif 'youtube' in self.query:
                    speak('what should I search for?')
                    topic = self.takeCommandMic()
                    pywhatkit.playonyt(topic)

                elif 'documents' in self.query or 'document' in self.query:
                    print("Opening Documents")
                    speak("Opening Documents")
                    document = 'path name goes here'
                    os.startfile(os.path.join(document))
    
                elif 'desktop' in self.query:
                    print("Opening Desktop")
                    speak("Opening Desktop")
                    desktop = 'path name goes here'
                    os.startfile(os.path.join(desktop))

                elif 'downloads' in self.query or 'download' in self.query:
                    print("Opening Downloads")
                    speak("Opening Downloads")
                    downloads = 'path name goes here'
                    os.startfile(os.path.join(downloads))

                elif 'powerpoint' in self.query:
                    print("Opening Microsoft PowerPoint")
                    speak("Opening Microsoft PowerPoint")
                    powerpoint = '.exe path name goes here'
                    os.startfile(os.path.join(powerpoint))

                elif 'word' in self.query:
                    print("Opening Microsoft Word")
                    speak("Opening Microsoft Word")
                    word = '.exe path name goes here'
                    os.startfile(os.path.join(word))

                elif 'excel' in self.query:
                    print("Opening Microsoft Excel")
                    speak("Opening Microsoft Excel")
                    excel = '.exe path name goes here'
                    os.startfile(os.path.join(excel))

                elif 'notepad' in self.query:
                    print("Opening Notepad")
                    speak("Opening Notepad")
                    notepad = '.exe path name goes here'
                    os.startfile(os.path.join(notepad))

                elif 'command' in self.query:
                    print("Opening Command Prompt")
                    speak("Opening Command Prompt")
                    commandprompt = '.lnk path name goes here'
                    os.startfile(os.path.join(commandprompt))

                elif 'weather' in self.query:
            
                    url= 'http://api.openweathermap.org/data/2.5/weather?q=mumbai&units=imperial&appid=xxx' # add your API key in place of xxx
                    res= requests.get(url)
                    data= res.json()
                    weather= data['weather'][0]['main']
                    temp = data['main']['temp']
                    desp= data['weather'][0]['description']
                    temp= round((temp-32)*5/9)
                    print(weather)
                    print(temp)
                    print(desp)
                    speak('Temperature : {} degree celcius'.format(temp))
                    speak('Weather is {}'.format(desp))

                elif 'news' in self.query:
                    speak('What topic do you need the news on?')
                    topic = self.takeCommandMic()
                    news(topic)

                elif 'joke' in self.query:
                    speak(pyjokes.get_joke())
                
                elif 'screenshot' in self.query:
                    ss()

                elif 'camera' in self.query:
                    open_camera()
                    
                elif 'location' in self.query:
                    My_Location()

                elif 'music' in self.query:
                    music='path name goes here'
                    songs= os.listdir(music)
                    os.startfile(os.path.join(music,songs[0]))

                elif 'far' in self.query:
                    Place=self.query[-1]
                    GoogleMaps(Place)
                    
                elif 'logout' in self.query or 'log' in self.query:
                    os.system("shutdown -l")
                
                elif 'shutdown' in self.query:
                    os.system("shutdown /s /t 1")

                elif 'restart' in self.query:
                    os.system("shutdown /r /t 1")
                
                else:
                    speak("I'm currently in learning mode. I'll soon get responses for your queries")
        
startExecution= MainThread()

class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.startTask)
        self.ui.pushButton_2.clicked.connect(self.close)
            
    def startTask(self):
        self.ui.movie=QtGui.QMovie("Aqua.gif") # add path name to GIF file here
        self.ui.assistantUi.setMovie(self.ui.movie)
        self.ui.movie.start()
        startExecution.start()

app = QApplication(sys.argv)
jarvis=Main()
jarvis.show()
sys.exit(app.exec_())