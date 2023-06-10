# importing libraries
import pyttsx3
import speech_recognition as sr
import pywhatkit
import sounddevice as sd
import soundfile as sf
from bs4 import BeautifulSoup
import requests
from PIL import Image
from io import BytesIO
from googleapiclient.discovery import build
from googletrans import Translator

tts_engine = pyttsx3.init()

#fct to speak
def speak(text, language):

    """Convert the given text to speech in the specified language and play it to the user."""
    tts_engine.setProperty('voice', language)
    tts_engine.say(text)
    tts_engine.runAndWait()

#fct to record audio
def record_audio(duration=5):

    fs = 44100
    print("Listening...")
    audio = sd.rec(int(duration * fs), samplerate=fs, channels=1)
    sd.wait()
    file_path = 'query.wav'
    sf.write(file_path, audio.flatten(), fs)
    return file_path

#fct to detect intent
def detect_intent(file_path):

    recognizer = sr.Recognizer()
    with sr.AudioFile(file_path) as source:
        audio_data = recognizer.record(source)
        query = recognizer.recognize_google(audio_data, language=language)
    return query

#fct to get article(web scraping)
def get_article(language_choice):
    if language_choice == 1:
        url = "https://en.hespress.com/tag/headlines"
    else:
        url = "https://fr.hespress.com/tag/a-la-une"
    headers = {
        "User-Agent":"µMozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"
    }
    r = requests.get(url,headers=headers)
    soup = BeautifulSoup(r.text,'html.parser')
    data = soup.find_all(class_ = 'stretched-link')
    link = data[0].get('href')

    r1 = requests.get(link,headers=headers)
    soup1 = BeautifulSoup(r1.text,'html.parser')
    paragraphs = soup1.find_all('p')
    article = paragraphs[0].text +'\n'+ paragraphs[1].text +'.....'
    return article
 


developer_key = 'AIzaSyCrEUsPVEa2T9w8I79iGWDdksZ51kIFkj4'
cx = 'e37d69a0e131f4987'

def fetch_images(query):
    #using google custom search api we'll search for images
    service = build("customsearch", "v1", developerKey=developer_key)
    results = service.cse().list(q=query, cx=cx, searchType='image').execute()
    images = results.get('items', [])
    return images

def process_query(query):
    
    if language_choice == '2':
        translator = Translator()
        query = translator.translate(query, src='fr', dest='en').text

    if "youtube" in query.lower():
        pywhatkit.playonyt(query)

    elif "hespress" in query.lower():
        article = get_article(language_choice)
        if choice_audio_text == '2':
            print(article)
        else:
            speak(article, language)

    elif "image" in query.lower() or "photo" in query.lower() or "picture" in query.lower():
        if choice_audio_text =='2':
            if language_choice == '2':
                num_images = int(input("Combien d'images voulez-vous ? (Max 10): "))
            else:
                num_images = int(input("How many images do you want? (Max 10): "))
        else:
            if language_choice == '2':
                speak("Combien d'images voulez-vous ? (Max 10)", language)
            else:
                speak("How many images do you want? (Max 10)", language)
            num_images = int(input("Your answer: "))
        
        images = fetch_images(query)
        for i, image in enumerate(images[:num_images]):
            try:
                image_url = image['link']
                response = requests.get(image_url)
                img = Image.open(BytesIO(response.content))
                img.show()
            except Exception as e:
                print(f'Error opening image: {e}')
    else:

        pywhatkit.search(query)

tts_engine = pyttsx3.init()

language_choice = input("Enter 1 for English and 2 for French: ")

if language_choice == '1':

    language = 'en-US'

else:

    language = 'fr-FR'

choice_audio_text = input("Enter 1 for audio and 2 for text: ")

if choice_audio_text == '1':

    if language == 'en-US':
        speak("Welcome to PTD", language)
        speak("You should mention YouTube in your query if you want to search on it.", language)
        speak("For pictures use photo in French and picture or image in English.", language)
        speak("To get the latest article in Hespress say: HESPRESS.", language)
    else:
        speak("Bienvenue à PTD bot", language)
        speak("Vous devez mentionner YouTube dans votre requête si vous souhaitez y effectuer une recherche.", language)
        speak("Pour les images, utilisez photo en français et image ou photo en anglais.", language)
        speak("Pour obtenir le dernier article dans Hespress, dites: HESPRESS.", language)
        
    print("Listening...")
    file_path = record_audio()
    query = detect_intent(file_path)
    print(f"You said: {query}")
    process_query(query)
    print('\n')
else:

    print("\t\t\t***********Welcome to PTD bot***********")
    print("****************************************************************************************************************")
    print("********************* You should mention YouTube in your query if you want to search on it *********************")
    print("****************************************************************************************************************")
    print("********* Vous devez mentionner YouTube dans votre requête si vous souhaitez y effectuer une recherche *********")
    print("****************************************************************************************************************")
    print("************************* For pictures use photo in french and picture or image in english *********************")
    print("****************************************************************************************************************")
    print("************************* Pour les images, utilisez photo en français et image ou photo en anglais *************")
    print("*****************************************************************************************************************")
    print("********************************************* VÉRIFIEZ VOTRE CONNEXION ******************************************")
    print("*****************************************************************************************************************")
    print("********************************************* CHECK YOUR CONNECTION *********************************************")
    print("****************************************************************************************************************")
    print("***************************** To get the latest article in Hespress say : HESPRESS ******************************")
    print("*****************************************************************************************************************")
    print("***************************** Pour obtenir le dernier article dans Hespress, dites : HESPRESS *******************")
    print("*****************************************************************************************************************")

    if language_choice == '1':
        message = input("How can I help you? ")
    else:
        message = input("Comment puis-je vous aider ? ")

    process_query(message)
