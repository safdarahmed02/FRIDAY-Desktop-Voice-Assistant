import sys
import pyjokes #this is for jokes
import pyttsx3
import time
import speech_recognition as sr
import datetime
import requests
import googlesearch
import json
from bs4 import BeautifulSoup
import os
import pyautogui
from PIL import Image
import pywhatkit
import webbrowser
import wikipedia
import smtplib


engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)


def speak(audio):
    engine.say(audio)
    print(audio)
    engine.runAndWait()


def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("listening...")
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source)  # adjust for ambient noise
        while True:
            audio = r.listen(source, timeout=5, phrase_time_limit=8)

            try:
                print("Recognizing...")
                query = r.recognize_google(audio, language='en-in')
                print(f"user said: {query}")
                return query
            except sr.UnknownValueError:
                speak("Sorry, I didn't catch that. Could you please repeat?")
                print("listening...")
            except sr.RequestError as e:
                speak("Sorry, I'm having trouble. Please try again later.")
                print("listening...")
                break
    return "none"


def wish():
    hour = int(datetime.datetime.now().hour)
    tt = time.strftime("%I:%M %p")

    if 0 <= hour <= 12:
        speak(f"Good morning, its {tt}")
    elif 12 <= hour <= 18:
        speak(f"Good afternoon, its {tt}")
    else:
        speak(f"Good evening, its {tt}")
    speak("How may I assist you")


def news(source='techcrunch', count=5):
    api_key = "YOUR_API_KEY_HERE"
    main_url = f'http://newsapi.org/v2/top-headlines?sources={source}&apiKey={api_key}'

    main_page = requests.get(main_url).json()
    articles = main_page["articles"][:count]
    for i, article in enumerate(articles):
        speak(f"Headline {i+1}: {article['title']}")


def scrapeQuotes():
    url = 'http://quotes.toscrape.com/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    quotes = soup.find_all('span', class_='text')

    for quote in quotes:
        print(quote.text)


SCREENSHOT_DIR = "C:/Users/Savita Pathak/Pictures/Screenshots"


def take_screenshot():
    now = datetime.datetime.now()
    timestamp = now.strftime("%Y-%m-%d %H-%M-%S")
    filename = f"screenshot_{timestamp}.png"
    image_path = os.path.join(SCREENSHOT_DIR, filename)
    image = pyautogui.screenshot()
    image.save(image_path)
    Image.open(image_path).show()


def open_notepad():
    notepad_path = r"C:\Windows\system32\notepad.exe"
    os.startfile(notepad_path)


def write_notepad():
    speak("What do you want to write in Notepad?")
    content = takecommand()

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"notepad_{timestamp}.txt"
    filepath = os.path.join(os.getcwd(), filename)

    with open(filepath, "w") as f:
        f.write(content)

    os.startfile(filepath)


def tell_joke():
    joke = pyjokes.get_joke()
    print(joke)
    speak(joke)



def play_youtube():
    speak("What do you want me to search on YouTube?")
    search_query = takecommand()
    speak(f"Playing {search_query} on YouTube")
    pywhatkit.playonyt(search_query)


def google_search(query):
    speak(f"Searching Google for {query}")
    query = query.replace(" ", "+")
    url = f"https://www.google.com/search?q={query}"
    webbrowser.get().open(url)


def search_wikipedia(query):
    try:
        results = wikipedia.search(query)
        page = wikipedia.page(results[0])
        summary = wikipedia.summary(page.title, sentences=2)
        print(summary)
        speak(summary)
    except wikipedia.exceptions.DisambiguationError as e:
        speak(f"Multiple results found for {query}. Please specify the query further.")
    except wikipedia.exceptions.PageError as e:
        speak(f"Page for {query} not found on Wikipedia.")


def send_email(email_address):
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login("safdarahmed9999@gmail.com", "chpduhtenprzqfkv")
    speak("What should be the subject of this email?")
    subject = takecommand()
    speak("What content do you want?")
    message = takecommand()
    username = email_address.split("@gmail.com")[0]
    message = f"Subject: {subject}\n\nDear {username},\n\n{message}"
    s.sendmail("safdarahmed9999@gmail.com", email_address, message)
    speak("Email sent successfully!")




def get_weather(city):
    api_key = "b7a69dcee9468dce40ca14e1cd980aca"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    data = json.loads(response.text)
    if data["cod"] != "404":
        # Extracting relevant information from data
        weather = data["weather"][0]["description"]
        temperature = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]
        humidity = data["main"]["humidity"]
        # Generating the output string
        output = f"The weather in {city} is {weather}, with a temperature of {temperature} degrees Celsius, and it feels like {feels_like} degrees Celsius. The humidity is {humidity} percent."
        return output
    else:
        return f"Sorry, {city} not found. Please try again with a valid city name."



def find_youtube_channel(query):
    search_results = googlesearch.search(query, num_results=10)
    for result in search_results:
        if "youtube.com/channel/" in result:
            channel_id = result.split("/channel/")[1]
            channel_url = f"https://www.youtube.com/channel/{channel_id}"
            response = requests.get(channel_url)
            if response.status_code == 200:
                channel_name = response.text.split("<title>")[1].split(" - YouTube</title>")[0]
                return channel_name, channel_url
    return None


def open_control_panel():
    os.system("control")


def set_reminder():
    speak("What do you want me to remind you about?")
    reminder = takecommand()
    speak("In how many minutes should I remind you?")
    mins = takecommand()
    mins = int(mins.replace(' ', ''))
    secs = mins * 60
    time.sleep(secs)
    speak(f"Reminder: {reminder}")



def power(mode):
    if mode == "restart":
        os.system("shutdown /r /t 1")
    elif mode == "sleep":
        os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
    elif mode == "shutdown":
        os.system("shutdown /s /t 1")
    else:
        speak("Invalid power mode. Please choose from 'restart', 'sleep', or 'shutdown'.")


if __name__ == "__main__":
    wish()
    while True:
        query = takecommand().lower()

        if "open notepad" in query:
            npath = "C://Windows//system32//notepad.exe"
            os.startfile(npath)


        elif "no thanks" in query:
            speak("thanks for using me sir, have a good day.")
            sys.exit()


        elif "play music" in query:
            music_dir = "C://Users//Username//Music"
            songs = os.listdir(music_dir)
            os.startfile(os.path.join(music_dir, songs[0]))


        elif "what's the time" in query or "tell me the time" in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"Sir, the time is {strTime}")


        elif "news" in query:
            news()
            break


        elif "quotes" in query:
            scrapeQuotes()
            break


        elif "screenshot" in query:
            take_screenshot()
            speak("Screenshot taken!")
            break


        elif "open notepad" in query:
            open_notepad()
            speak("Opening Notepad!")
            write_notepad()
            break


        elif "tell me a joke" in query:
            tell_joke()
            break

        elif "play youtube" in query:
            play_youtube()
            break


        elif "google" in query:
            speak("What do you want me to search on Google?")
            search_query = takecommand()
            google_search(search_query)
            break


        elif "wikipedia" in query:
            speak("What do you want to know from wikipedia?")
            query = takecommand()
            search_wikipedia(query)
            break


        elif "power" in query:
            speak("Which mode do you want to activate? 'restart', 'sleep', or 'shutdown'?")
            mode = takecommand().lower()
            power(mode)
            speak(f"{mode} mode activated!")
            break


        elif "send email" in query:
            #speak("Whom should I send this email to?")
            #recipient = takecommand()
            speak("What content do you want?")
            message = takecommand()
            send_email(message)
            speak("Email sent successfully!")
            break

        elif "weather" in query:
            speak("Sure, which city's weather do you want to know?")
            city = takecommand().lower()
            weather_info = get_weather(city)
            speak(weather_info)
            break


        elif "set reminder" in query:
            set_reminder()
            speak("reminded  successfully")
            break


        elif "open settings" in query:
            open_control_panel()
            speak("Opening settings.")
            break
