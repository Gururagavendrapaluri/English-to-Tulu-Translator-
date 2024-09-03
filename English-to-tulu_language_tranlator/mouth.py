import asyncio
# multiple lightweight tasks can run concurrently with minimal memory
import threading #enbles to different parts of programs run concurrently a
import os
import edge_tts # generate speech from text and run it as an audio file 
import pygame # Pygame provides modules for sound, graphics, and input handling,

#voice = "en-AU-WilliamNeural"
#voice="en-US-JessaNeural" #Narrator
#voice="en-IN-PrabhatNeural"
voice="en-IN-NeerjaNeural"

#kannada
#voice="kn-IN-GaganNeural"
#voice="kn-IN-SapnaNeural"

#telugu
#voice="te-IN-MohanNeural"
#voice="te-IN-ShrutiNeural"

buffer_size = 1024  # Defining the buffer size for audio processing or file operations.

'''
This code attempts to securely remove a file by first clearing its contents and then deleting it, 
retrying up to three times if an error occurs.
'''
def remove_file(file_path):
    """
    This function attempts to securely remove a file by first clearing its contents 
    and then deleting it, retrying up to three times if an error occurs.
    """
    max_attempts = 3  # Maximum number of retry attempts.
    attempts = 0  # Initializing the number of attempts.
    while attempts < max_attempts:
        try:
            # Open the file in write-binary mode ('wb') to clear its contents.
            with open(file_path, "wb"):
                pass
            # Remove the file from the filesystem.
            os.remove(file_path)
            break  # Exit the loop if the file is successfully removed.
        except Exception as e:
            # Print the error message if an exception occurs.
            print(f"error : {e}")
            attempts += 1  # Increment the attempt counter.

async def amain(TEXT, output_file) -> None:
    """
    This asynchronous function communicates a text-to-speech conversion and plays the resulting audio file.
    """
    try:
        # Initialize text-to-speech communication and save the output to a file.
        communicate = edge_tts.Communicate(TEXT, voice)
        await communicate.save(output_file)
        # Start a new thread to play the audio file.
        thread = threading.Thread(target=play_audio, args=(output_file,))
        thread.start()  # Start the audio playback thread.
        thread.join()  # Wait for the audio playback thread to complete.
    except Exception as e:
        # Print the error message if an exception occurs.
        print(f"error: {e}")
    finally:
        # Remove the audio file after playback.
        remove_file(output_file)

def play_audio(file_path):
    """
    This function initializes the pygame library, loads an audio file, and plays it.
    """
    try:
        pygame.init()  # Initialize the pygame library.
        pygame.mixer.init()  # Initialize the pygame mixer for audio playback.
        sound = pygame.mixer.Sound(file_path)  # Load the audio file.
        sound.play()  # Play the audio file.
        # Wait until the audio playback is finished.
        while pygame.mixer.get_busy():
            pygame.time.wait(10)
        pygame.quit()  # Quit pygame after playback.
    except Exception as e:
        # Print the error message if an exception occurs.
        print(f"error: {e}")

def speak(TEXT, output_file=None):
    """
    This function handles text-to-speech conversion and playback.
    """
    # If no output file is specified, use a default file path.
    if output_file is None:
        output_file = f"{os.getcwd()}/speak.mp3"
    # Run the asynchronous amain function to process and play the speech.
    asyncio.run(amain(TEXT, output_file))
























# buffer_size = 1024


# '''
# This code attempts to securely remove a file by first clearing its contents and then deleting it, 
# retrying up to three times if an error occurs.
# '''
# def remove_file(file_path):
#     max_attempts = 3
#     attempts = 0
#     while attempts < max_attempts:
#         try:
#             with open(file_path, "wb"):
#                 pass
#             os.remove(file_path)
#             break
#         except Exception as e:
#             print(f"error : {e}")
#             attempts += 1

# async def amain(TEXT, output_file) -> None: 
#     try:
#         communicate = edge_tts.Communicate(TEXT, voice)
#         await communicate.save(output_file)
#         thread = threading.Thread(target=play_audio, args=(output_file,))
#         thread.start()
#         thread.join()
#     except Exception as e:
#         print(f"error: {e}")
#     finally:
#         remove_file(output_file)

# def play_audio(file_path):
#     try:
#         pygame.init()
#         pygame.mixer.init()
#         sound = pygame.mixer.Sound(file_path)
#         sound.play()
#         while pygame.mixer.get_busy():
#             pygame.time.wait(10)
#         pygame.quit()
#     except Exception as e:
#         print(f"error: {e}")

# def speak(TEXT, output_file=None):
#     if output_file is None:
#         output_file = f"{os.getcwd()}/speak.mp3"
#     asyncio.run(amain(TEXT, output_file))

