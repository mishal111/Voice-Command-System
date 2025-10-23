import speech_recognition as sr
import os
from playsound3 import playsound
import threading

recognizer=sr.Recognizer()
wake_word="friday"

def wake_command():
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio=recognizer.listen(source,phrase_time_limit=5)
        try:
            text=recognizer.recognize_google(audio).lower()
            print(text)
            if text==wake_word:
                playsound("/home/Mishal/Downloads/Voicy.mp3")
                listen_command()     
                
        except TimeoutError:
            print("Connection error")
        
        except ValueError:
            print("Speech not clear")

def listen_command():
    
    with sr.Microphone() as source:
        print("Waiting for command")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source,timeout=5,phrase_time_limit=5)
    
    try:
        command=recognizer.recognize_google(audio).lower()
        if command=="open firefox":
            os.system("exec /usr/lib/firefox/firefox")
            wake_command()
        elif command=="open spotify":
            os.system("exec /var/lib/snapd/snap/bin/spotify")
            wake_command()
        elif command=="open code":
            os.system("exec /opt/visual-studio-code/bin/code/")
            wake_command()
        elif command=="terminate":
            print("Program terminated")
            os._exit(0) 

    except TimeoutError:
        print("Connection Issue")

    except ValueError:
        print("Speech not clear")

threading.Thread(target=wake_command(),daemon=True).start()
