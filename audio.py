import random
import time
import speech_recognition as sr

powerUp = True

def powerUp():
    #Right now 
    return powerUp

#Below is speech code



#Shift so it captures many small word segents
def spellCast():
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()
    with microphone as source:
        
        recognizer.adjust_for_ambient_noise(source)

        #audio = recognizer.listen(source)

        audio = recognizer.listen(source, timeout=4, phrase_time_limit=4)
        word = None
        try:
            word = recognizer.recognize_google(audio)
        except sr.UnknownValueError:
            # Error handling for when the speech is unintelligible
            print("Google Speech Recognition could not understand audio")
            
        except sr.RequestError as e:
            # Error handling for when there's a problem with the request to Google's service
            print(f"Could not request results from Google Speech Recognition service; {e}")
        
       
        if(word != None):
            return word
        else: return "fail"
"""
def recognize_speech_from_mic(recognizer, microphone):
    # check that recognizer and microphone arguments are appropriate type
    if not isinstance(recognizer, sr.Recognizer):
        raise TypeError("`recognizer` must be `Recognizer` instance")

    if not isinstance(microphone, sr.Microphone):
        raise TypeError("`microphone` must be `Microphone` instance")

    # adjust the recognizer sensitivity to ambient noise and record audio
    # from the microphone
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

        

    # set up the response object
    response = {
        "success": True,
        "error": None,
        "transcription": None
    }

    # try recognizing the speech in the recording
    # if a RequestError or UnknownValueError exception is caught,
    #     update the response object accordingly
    try:
        response["transcription"] = recognizer.recognize_google(audio)
    except sr.RequestError:
        # API was unreachable or unresponsive
        response["success"] = False
        response["error"] = "API unavailable"
    except sr.UnknownValueError:
        # speech was unintelligible
        response["error"] = "Unable to recognize speech"
    return response

if __name__ == "__main__":
    # set the list of words, maxnumber of guesses, and prompt limit
    WORDS = ["Fire", "Water"]
    NUM_GUESSES = 3
    PROMPT_LIMIT = 5

    # create recognizer and mic instances
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    # get a random word from the list
    word = random.choice(WORDS)

    print(recognize_speech_from_mic(recognizer, microphone))

    """