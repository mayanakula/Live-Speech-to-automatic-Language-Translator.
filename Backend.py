# without background noise cancellation
#import speech_recognition as sr # type: ignore

# # Initialize the recognizer
# recognizer = sr.Recognizer()

# # Function to capture live speech and convert it to text
# def recognize_speech_from_mic():
#     with sr.Microphone() as source:
#         print("Listening...")
#         # Adjust the recognizer sensitivity to ambient noise levels
#         recognizer.adjust_for_ambient_noise(source)
#         # Capture the audio
#         audio = recognizer.listen(source)
        
#         try:
#             # Recognize speech using Google Web Speech API
#             text = recognizer.recognize_google(audio)
#             print("You said: " + text)
#         except sr.RequestError:
#             print("API unavailable")
#         except sr.UnknownValueError:
#             print("Unable to recognize speech")

# if __name__ == "__main__":
#     recognize_speech_from_mic()
###with background noise cancellation
# import speech_recognition as sr
# import noisereduce as nr
# import numpy as np
# import io

# # Initialize the recognizer
# recognizer = sr.Recognizer()

# # Function to capture live speech, reduce noise, and convert it to text
# def recognize_speech_from_mic():
#     with sr.Microphone() as source:
#         print("Listening... Please speak into the microphone.")
#         # Adjust the recognizer sensitivity to ambient noise levels
#         recognizer.adjust_for_ambient_noise(source)
#         # Capture the audio
#         audio = recognizer.listen(source)

#         try:
#             # Convert the audio to a NumPy array
#             audio_data = np.frombuffer(audio.get_raw_data(), dtype=np.int16)
#             # Perform noise reduction
#             reduced_noise_audio = nr.reduce_noise(y=audio_data, sr=source.SAMPLE_RATE)
#             # Convert the NumPy array back to audio data
#             reduced_noise_audio_io = io.BytesIO()
#             reduced_noise_audio_io.write(reduced_noise_audio.tobytes())
#             reduced_noise_audio = sr.AudioData(reduced_noise_audio_io.getvalue(), source.SAMPLE_RATE, 2)

#             # Recognize speech using Google Web Speech API
#             text = recognizer.recognize_google(reduced_noise_audio)
#             print("You said: " + text)
#         except sr.RequestError:
#             print("Could not request results; check your network connection.")
#         except sr.UnknownValueError:
#             print("Could not understand the audio.")

# if __name__ == "__main__":
#     recognize_speech_from_mic()
###With Google translation
# import speech_recognition as sr
# import noisereduce as nr
# import numpy as np
# import io
# from googletrans import Translator

# # Initialize the recognizer and translator
# recognizer = sr.Recognizer()
# translator = Translator()

# # Function to capture live speech, reduce noise, recognize speech, and translate text
# def recognize_and_translate_speech():
#     with sr.Microphone() as source:
#         print("Listening... Please speak into the microphone.")
#         # Adjust the recognizer sensitivity to ambient noise levels
#         recognizer.adjust_for_ambient_noise(source)
#         # Capture the audio
#         audio = recognizer.listen(source)
        
#         try:
#             # Convert the audio to a NumPy array
#             audio_data = np.frombuffer(audio.get_raw_data(), dtype=np.int16)
#             # Perform noise reduction
#             reduced_noise_audio = nr.reduce_noise(y=audio_data, sr=source.SAMPLE_RATE)
#             # Convert the NumPy array back to audio data
#             reduced_noise_audio_io = io.BytesIO()
#             reduced_noise_audio_io.write(reduced_noise_audio.tobytes())
#             reduced_noise_audio = sr.AudioData(reduced_noise_audio_io.getvalue(), source.SAMPLE_RATE, 2)
            
#             # Recognize speech using Google Web Speech API
#             text = recognizer.recognize_google(reduced_noise_audio)
#             print("You said: " + text)
            
#             # Translate the recognized text
#             translated_text = translator.translate(text, dest='en')  # Translate to Spanish ('en'), can change to any language code
#             print("Translated text: " + translated_text.text)
#         except sr.RequestError:
#             print("Could not request results; check your network connection.")
#         except sr.UnknownValueError:
#             print("Could not understand the audio.")
#         except Exception as e:
#             print(f"An error occurred: {e}")

# if __name__ == "__main__":
#     recognize_and_translate_speech()
import speech_recognition as sr
import noisereduce as nr
import numpy as np
import io
from googletrans import Translator
import pyttsx3
from textblob import TextBlob

# Initialize the recognizer, translator, and text-to-speech engine
recognizer = sr.Recognizer()
translator = Translator()
tts_engine = pyttsx3.init()

# Function to capture live speech, reduce noise, recognize speech, and translate text
def recognize_and_translate_speech():
    with sr.Microphone() as source:
        print("Listening... Please speak into the microphone.")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
        
        try:
            audio_data = np.frombuffer(audio.get_raw_data(), dtype=np.int16)
            reduced_noise_audio = nr.reduce_noise(y=audio_data, sr=source.SAMPLE_RATE)
            reduced_noise_audio_io = io.BytesIO()
            reduced_noise_audio_io.write(reduced_noise_audio.tobytes())
            reduced_noise_audio = sr.AudioData(reduced_noise_audio_io.getvalue(), source.SAMPLE_RATE, 2)
            
            text = recognizer.recognize_google(reduced_noise_audio)
            print("You said: " + text)

            translated_text = translator.translate(text, dest='en')  # Translate to Telugu ('te')
            print("Translated text: " + translated_text.text)

            tts_engine.say(translated_text.text)
            tts_engine.runAndWait()
            
            detect_and_express_emotion(translated_text.text)
            
        except sr.RequestError:
            print("Could not request results; check your network connection.")
        except sr.UnknownValueError:
            print("Could not understand the audio.")
        except Exception as e:
            print(f"An error occurred: {e}")

# Function to detect and express emotion
def detect_and_express_emotion(text):
    blob = TextBlob(text)
    sentiment = blob.sentiment
    print(f"Detected emotion: {sentiment}")
    if sentiment.polarity > 0:
        tts_engine.say("It sounds like you're feeling positive!")
    elif sentiment.polarity < 0:
        tts_engine.say("It sounds like you're feeling negative.")
    else:
        tts_engine.say("It sounds like you're feeling neutral.")
    tts_engine.runAndWait()

if __name__ == "__main__":
    recognize_and_translate_speech()

