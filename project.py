import speech_recognition as sr
from deep_translator import GoogleTranslator
from gtts import gTTS
import os

# Initialize recognizer
recognizer = sr.Recognizer()

# Take voice input
with sr.Microphone() as source:
    print("Adjusting for ambient noise...")
    recognizer.adjust_for_ambient_noise(source, duration=1)
    print("Speak something...")
    try:
        audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
    except sr.WaitTimeoutError:
        print("Listening timed out. No speech detected.")
        exit()

try:
    # Convert speech to text
    text = recognizer.recognize_google(audio)
    print("You said:", text)

    # Translate text (English → French example)
    target_lang = "fr"
    translated_text = GoogleTranslator(source='auto', target=target_lang).translate(text)

    print("Translated:", translated_text)

    # Convert translated text to speech
    tts = gTTS(text=translated_text, lang=target_lang)
    tts.save("translated.mp3")

    # Play translated voice
    os.system("start translated.mp3")

except sr.UnknownValueError:
    print("Error: Could not understand the audio.")
except sr.RequestError as e:
    print(f"Error: Could not request results from Google Speech Recognition service; {e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")