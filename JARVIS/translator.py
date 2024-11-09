import speech_recognition as sr
from googletrans import Translator, LANGUAGES
from gtts import gTTS
import io
import pyttsx3
import pygame

# Initialize recognizer and TTS engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()

# Initialize pygame mixer
pygame.mixer.init()

def get_language_code(language_name):
    """
    Retrieve language code from googletrans LANGUAGES dictionary.
    """
    language_name = language_name.lower()  # Make case-insensitive
    for code, lang in LANGUAGES.items():
        if language_name in lang.lower():
            return code
    return None

def capture_speech(prompt):
    """
    Capture speech from the microphone and recognize it as text.
    """
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)
        print(prompt)
        engine.say(prompt)
        engine.runAndWait()
        
        try:
            # Listen until speech starts, with a phrase limit of 5 seconds
            audio = recognizer.listen(source, timeout=None, phrase_time_limit=5)
            result = recognizer.recognize_google(audio, language='en')
            print(f"Recognized Speech: {result}")
            return result
        except sr.WaitTimeoutError:
            print("Listening timed out while waiting for phrase to start.")
            engine.say("Listening timed out. Please try again.")
            engine.runAndWait()
        except sr.UnknownValueError:
            print("Could not understand the audio.")
            engine.say("I could not understand the audio.")
            engine.runAndWait()
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
            engine.say("There was an error with the request.")
            engine.runAndWait()
        return None

def play_audio_from_gtts(text, language_code):
    """
    Convert text to speech using gTTS, and play it directly using pygame.
    """
    try:
        tts = gTTS(text=text, lang=language_code)
        audio_fp = io.BytesIO()  # Use an in-memory bytes buffer
        tts.write_to_fp(audio_fp)
        audio_fp.seek(0)  # Reset buffer to the start
        
        # Load and play the audio from the buffer
        pygame.mixer.music.load(audio_fp, 'mp3')
        pygame.mixer.music.play()
        
        # Wait until the audio has finished playing
        while pygame.mixer.music.get_busy():
            continue
        
    except Exception as e:
        print(f"Error playing audio: {e}")
        engine.say("There was an error playing the audio.")
        engine.runAndWait()

def translate_text(text):
    """
    Prompt the user for a language and translate the text using Google Translate.
    """
    engine.say("Your speech has been captured successfully. Which language would you like to convert to?")
    engine.runAndWait()
    
    language_name = capture_speech("Please say the language name to translate to.")  # Capture the language name
    if language_name:
        language_code = get_language_code(language_name)
        
        if language_code:
            try:
                translator = Translator()
                translation = translator.translate(text, dest=language_code)
                translated_text = translation.text
                print(f"Translated Text: {translated_text}")

                # Play the translated text directly
                play_audio_from_gtts(translated_text, language_code)
            except Exception as e:
                print(f"Translation error: {e}")
                engine.say("There was an error with translation.")
                engine.runAndWait()
        else:
            print("Language not found. Please enter a valid language name.")
            engine.say("Language not found. Please try again.")
            engine.runAndWait()
    else:
        print("No language name recognized.")
        engine.say("No language name was recognized. Please try again.")
        engine.runAndWait()

# Main function to capture and translate speech
def main_for_speech():
    print("Speak a sentence you want to translate.")
    engine.say("Speak a sentence you want to translate.")
    engine.runAndWait()
    
    # Capture speech
    captured_text = capture_speech("Listening for your sentence...")
    
    # Translate and speak the translated text
    if captured_text:
        translate_text(captured_text)
    else:
        print("No speech detected. Please try again.")
        engine.say("No speech detected. Please try again.")
        engine.runAndWait()
