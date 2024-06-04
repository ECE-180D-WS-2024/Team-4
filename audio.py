import random
import time
import speech_recognition as sr

powerUp = True

def powerUp():
    #Right now 
    return powerUp

#Below is speech code



#Shift so it captures many small word segents
import speech_recognition as sr

def spellCast():
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)

        try:
            # Listen for the first phrase and extract it into audio data
            audio = recognizer.listen(source, timeout=4, phrase_time_limit=4)
            # Try to recognize the speech in the audio
            word = recognizer.recognize_google(audio, language="it-IT")
            return word

        except sr.WaitTimeoutError:
            # Handle the case where no speech was detected within the timeout limit
            print("No speech detected within the timeout period.")
            return "fail"

        except sr.UnknownValueError:
            # Error handling for when the speech is unintelligible
            print("Google Speech Recognition could not understand audio")
            return "fail"
            
        except sr.RequestError as e:
            # Error handling for when there's a problem with the request to Google's service
            print(f"Could not request results from Google Speech Recognition service; {e}")
            return "fail"
