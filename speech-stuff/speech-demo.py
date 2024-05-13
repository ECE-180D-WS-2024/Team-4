import time
import speech_recognition as sr

def recognize_activation_word(recognizer, microphone):

    # Adjust the recognizer sensitivity to ambient noise and record audio from the microphone

    print("Listening for activation words...")

    with microphone as source:

        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    # Attempt to recognize speech in the recording
    
    try:

        # Use Google Speech Recognition to recognize the speech in Italian
        transcription = recognizer.recognize_google(audio, language="it-IT")
        
        # Convert to lowercase for case-insensitive comparison
        return transcription.lower()
    
    except sr.UnknownValueError:

        # Unable to recognize speech
        print("UnknownValueError: Unable to recognize speech")
        return None

if __name__ == "__main__":

    # Create recognizer and microphone instances
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    while True:

        # Recognize the activation word
        activation_word = recognize_activation_word(recognizer, microphone)

        # Check if the activation word is "attivare", "iniziato", or "uscita"

        if activation_word == "attivare":
            print("Player one spell casted!")

        elif activation_word == "iniziato":
            print("Player two spell casted!")

        elif activation_word == "uscita":
            print("Exiting the program...")
            break

        elif activation_word is None:
            print("Sorry, I couldn't understand. Please try again.")

        else:
            print("Activation word not recognized. Please try again.")

        # Pause for a moment before continuing to listen
        time.sleep(1)