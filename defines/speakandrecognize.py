import speech_recognition as sr
from gtts import gTTS
import pyglet
import time
from time import sleep
import os


# HERE CONVERTS USER VOICE INPUT INTO MACHINE READABLE TEXT
def ask_ettibot():
    print("Speak Now . . .")

    r = sr.Recognizer()
    r.energy_threshold = 50
    r.dynamic_energy_threshold = False

    with sr.Microphone() as source:
        print("Listening....")
        audio = r.listen(source)  # phrase_time_limit=3)
        # Call LED lights here

        try:
            # Call LED lights here
            print("Recognising....")
            text = r.recognize_google(audio, language='en')
            print(text)

        except Exception as e:
            print("Exception " + str(e))
            return "none"

    return text


# HERE CONVERTS TEXT INTO VOICE OUTPUT
def speak(text, lang="en"):  # here audio is var which contain text
    # Call LED lights here
    tts = gTTS(text=text, lang=lang)
    filename = 'temp.mp3'
    tts.save(filename)
    music = pyglet.media.load(filename, streaming=False)
    music.play()
    sleep(music.duration)  # prevent from killing
    os.remove(filename)  # remove temporary file
