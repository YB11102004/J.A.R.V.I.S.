import os
import time
import pyttsx3
import pyautogui
import numpy as np

# Initialize text-to-speech engine
engine = pyttsx3.init()

def speak(text):
    """Function to make the assistant speak a given text."""
    engine.say(text)
    engine.runAndWait()

def search_contact(contact_name):
    """Search for a contact on WhatsApp Desktop using PyAutoGUI."""
    speak(f"Searching for {contact_name}")
    time.sleep(2)  # Wait for WhatsApp to load if not already open

    pyautogui.hotkey('ctrl','f')

    # Type the contact name in the search bar
    pyautogui.write(contact_name, interval=0.1)
    time.sleep(2)  # Wait for results to load

    # Select the contact (use Enter to select the first result)
    for key in ['tab','enter','enter']:
        pyautogui.press(key)
        time.sleep(2)
    time.sleep(1)

def send_message(contact_name,message_text):
    search_contact(contact_name)
    """Send a text message to a contact in the active chat."""
    speak("Typing message")
    # Type the message
    pyautogui.write(message_text, interval=0.1)
    time.sleep(1)

    # Send the message by pressing Enter
    pyautogui.press('enter')
    speak("Message sent")

def make_audio_call(contact_name):
    search_contact(contact_name)
    speak("Starting an audio call")
    search_contact(contact_name)
    for key in ['tab','tab','tab','tab','tab','tab','tab','tab','tab','tab','tab','enter']:
        pyautogui.press(key)
    time.sleep(1)

def make_video_call(contact_name):
    search_contact(contact_name)
    for key in ['tab','tab','tab','tab','tab','tab','tab','tab','tab','tab','enter']:
        pyautogui.press(key)
    time.sleep(1)