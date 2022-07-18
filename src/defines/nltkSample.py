import pygame
from time import sleep
from pygame import mixer
from gtts import gTTS
from mutagen.mp3 import MP3
import speech_recognition as sr

# nltk ====
import nltk
from nltk.tokenize import word_tokenize
from nltk import ne_chunk, pos_tag, word_tokenize
from nltk.tree import Tree
from nltk.tokenize.treebank import TreebankWordDetokenizer

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet


person_list = []
person_names=person_list
global name
name = ""

pygame.mixer.pre_init(22050, 16, 1, 4096) #frequency, size, channels, buffersize
pygame.mixer.init()
pygame.init()
energyThres = 301

r = sr.Recognizer()
m = sr.Microphone()

with m as source:
    r.adjust_for_ambient_noise(source)
    r.energy_threshold = energyThres
    
# function to convert the seconds into readable format
def convert(seconds):
    hours = seconds // 3600
    seconds %= 3600

    mins = seconds // 60
    seconds %= 60

    return hours, mins, seconds
        
# HERE CONVERTS TEXT INTO VOICE OUTPUT
def speak(text, lang="en"):  # here audio is var which contain text
    # Call LED lights here
    speaking = True
    tts = gTTS(text=text, lang=lang)
    filename = 'temp.mp3'
    tts.save(filename)
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()
    audio = MP3("temp.mp3")
    audio_info = audio.info
    length_in_secs = int(audio_info.length)
    hours, mins, seconds = convert(length_in_secs)
    sleep(seconds+0.7) 

# this is called from the background thread
def callback(recognizer, audio):
    
    # received audio data, now we'll recognize it using Google Speech Recognition
    try:
        # for testing purposes, we're just using the default API key
        # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        # instead of `r.recognize_google(audio)`
        text = recognizer.recognize_google(audio)
        print("Complete: " + text)
        
        global user_input
        user_input = text
        #print (text)
        stripWords = word_tokenize(text)
        stopWords = ["ai", "madam", "tutor", "athena", "thesis", "hi", "hello"]

        if any (i in stripWords for i in stopWords):
            result = [i for i in stripWords if not any([e for e in stopWords if e in i])] #this code removes the stopWords from stripWords
            recognizedWords(result)

    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))


def recognizedWords(text):
    print(text)
    print(f"Detokenized: {TreebankWordDetokenizer().detokenize(text).capitalize()}")
    
    example_sent = """This is a sample sentence
                  showing off the stop words filtration."""
    
    stop_words = set(stopwords.words('english'))
    stop_name = ['name', 'my', 'is', 'i', 'am']
    word_tokens = word_tokenize(example_sent)
    name_token = text
    
    
    filtered_sentence = [w for w in word_tokens if not w.lower() in stop_words]
    filtered_sentence = []
    
    for w in word_tokens:
        if w not in stop_words:
            filtered_sentence.append(w)
            
    filtered_name = [w for w in name_token if not w.lower() in stop_words]
    filtered_name = [w for w in name_token if not w.lower() in stop_name]
    filtered_name = []
    
    for w in name_token:
        if w not in stop_name:
            filtered_name.append(w)
      
    print(name_token)
    print(filtered_name)
    
    
    print(f"hi {TreebankWordDetokenizer().detokenize(filtered_name).capitalize()}")

stop_listening = r.listen_in_background(m, callback) #phrase_time_limit=10

