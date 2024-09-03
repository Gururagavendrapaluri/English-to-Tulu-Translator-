import speech_recognition as sr  # Importing the speech_recognition library for speech-to-text conversion.

def listen_and_print():
    """
    This function listens to the user's voice using the microphone and prints the recognized text.
    """
    # Initialize recognizer
    recognizer = sr.Recognizer()  # Creating a Recognizer object.
    
    # Use the default microphone as the audio source
    with sr.Microphone() as source:  # Using the microphone as the source for input.
        print("Listening for your query...")
        
        # Adjust for ambient noise
        recognizer.adjust_for_ambient_noise(source)  # Adjusting the recognizer sensitivity to ambient noise.
        
        # Set the timeout and phrase_time_limit for faster response
        try:
            # Listening for the user's input with a timeout of 5 seconds and a phrase time limit of 5 seconds.
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
        except sr.WaitTimeoutError:
            # Handling the case where the user did not speak within the timeout period.
            print("Listening timed out. Please try again.")
            return None
        except sr.RequestError as e:
            # Handling the case where there was an error with the request to the recognition service.
            print(f"Sorry, there was an error with the request: {e}")
            return None
        
        try:
            # Recognize speech using Google's speech recognition
            query = recognizer.recognize_google(audio)  # Using Google Web Speech API to recognize the speech.
            print(f"You said: {query}")  # Printing the recognized text.
            return query
        except sr.UnknownValueError:
            # Handling the case where the recognizer could not understand the audio.
            print("Sorry, I did not understand that.")
            return None
        except sr.RequestError as e:
            # Handling the case where there was an error with the request to the recognition service.
            print(f"Sorry, there was an error with the request: {e}")
            return None

