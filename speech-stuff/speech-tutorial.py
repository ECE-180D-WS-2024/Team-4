import time
import speech_recognition as sr
from fuzzywuzzy import fuzz

def recognize_activation_word(recognizer, microphone, word):
    while True:
        print(f"Please pronounce '{word}'...")
        with microphone as source:
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)

        try:
            # Use Google Speech Recognition to recognize the speech in Italian
            transcription = recognizer.recognize_google(audio, language="it-IT")
            # Convert to lowercase for case-insensitive comparison
            transcription = transcription.lower()
            
            # Calculate similarity score between recognized speech and target word
            similarity_score = fuzz.ratio(transcription, word)

            # Set a threshold score for acceptable recognition
            threshold = 70

            if similarity_score >= threshold:
                print(f"'{word}' pronounced successfully!")
                return True
            else:
                print(f"Sorry, I didn't catch '{word}' correctly. Please try again.")
        except sr.UnknownValueError:
            # Unable to recognize speech
            print("UnknownValueError: Unable to recognize speech")
            continue

if __name__ == "__main__":
    # Create recognizer and microphone instances
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    print("Welcome to the spell casting tutorial mode!")

    # Pronounce 'attivare'
    if recognize_activation_word(recognizer, microphone, "attivare"):
        # Pronounce 'iniziato'
        if recognize_activation_word(recognizer, microphone, "iniziato"):
            print("Exiting tutorial mode...")