import pygame
import pyaudio
import numpy as np
import threading
import time
import os
import pyttsx3
import speech_recognition as sr
from authentication import authenticate_user
from questions import respond_to_question
from datetime import datetime
from Spotify import search_song, play_song, pause_song
from Youtube import open_youtube, search_video
from translator import main_for_speech
from Whatsapp import search_contact, make_audio_call, make_video_call, send_message
from email_typing import email_details
from google_search import search_google

# Initialize PyAudio
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

p = pyaudio.PyAudio()
stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

# Initialize Pygame
pygame.init()
WIDTH, HEIGHT = 900, 700 
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jarvis Voice Assistant")
clock = pygame.time.Clock()

# Initialize the text-to-speech engine
engine = pyttsx3.init()

# Initialize the speech recognizer
recognizer = sr.Recognizer()

# Function to animate the circles (Visuals)
def animate_circles():
    global running_animation
    base_radius = 250
    max_radius = 270
    num_inner_circles = 7
    while running_animation:
        data = np.frombuffer(stream.read(CHUNK), dtype=np.int16)
        volume = np.linalg.norm(data)
        radius = base_radius + (volume / 3000) * (max_radius - base_radius)
        radius = min(max(radius, base_radius), max_radius)
        screen.fill((0, 0, 0))

        outer_color = (int(255 * (radius / max_radius)), 0, int(255 * (1 - radius / max_radius)))
        pygame.draw.circle(screen, outer_color, (WIDTH // 2, HEIGHT // 2), int(radius), width=5)

        for i in range(num_inner_circles):
            inner_radius = radius - (i + 1) * 10
            if inner_radius > 0:
                inner_color = (int(255 * (inner_radius / max_radius)), 0, int(255 * (1 - inner_radius / max_radius)))
                pygame.draw.circle(screen, inner_color, (WIDTH // 2, HEIGHT // 2), int(inner_radius), width=5)

        pygame.display.flip()
        clock.tick(30)

# Function to greet the user with speech
def greet_user():
    greeting_text = "At your service Ma'am!! How can I help you?"
    engine.say(greeting_text)
    engine.runAndWait()
    time.sleep(1)

# Function to listen for questions and respond verbally
def listen_and_respond():
    while True:
        with sr.Microphone() as source:
            print("Listening for your question...")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)

            try:
                question = recognizer.recognize_google(audio).lower()  # Convert the input to lowercase for easier matching
                print(f"You said: {question}")
                if "goodbye jarvis" in question:
                    engine.say("Goodbye!")
                    engine.runAndWait()
                    running_animation = False  # Stop the circle animation
                    break
                elif "write an email" in question:
                    email_id='anika.from.nowhere@gmail.com'
                    password='sztc amnl frfw uede'
                    email_details(email_id,password)    
                elif 'search in google for' in question:
                    query=question.replace("search in google for", "").strip()
                    search_google(query, num_results=5, open_top_result=False)
                elif "open spotify" in question:
                    engine.say("Opening Spotify.")
                    engine.runAndWait()
                    os.system('spotify')
                    time.sleep(10)
                elif "search" in question:
                    song_name=question.replace("search", "").strip()
                    search_song(song_name)
                elif "pause song" in question:
                    pause_song()
                elif "play song" in question:
                    play_song()
                elif "open youtube" in question:
                    open_youtube()
                    engine.say("Opening YouTube.")
                    engine.runAndWait()
                elif "search for" in question:
                    video_name = question.replace("search for", "").strip()  # Extract the video name
                    search_video(video_name)
                    engine.say(f"Searching for {video_name} on YouTube.")
                    engine.runAndWait()
                elif "open whatsapp" in question:
                    engine.say("Opening Whatsapp.")
                    engine.runAndWait()
                    os.startfile('whatsapp:')
                    time.sleep(10)
                elif "search contact" in question:
                    contact_name = question.replace("search contact", "").strip()
                    search_contact(contact_name)
                elif "send message" in question:
                    engine.say("Please say the contact name.")
                    engine.runAndWait()
                    with sr.Microphone() as source:
                        recognizer.adjust_for_ambient_noise(source)
                        audio = recognizer.listen(source)
                        try:
                            contact_name = recognizer.recognize_google(audio)
                            print(f"Contact name: {contact_name}")
                        except sr.UnknownValueError:
                            engine.say("Sorry, I couldn't understand the contact name.")
                            engine.runAndWait()
                            continue

                    # Ask for the message
                    engine.say(f"What message would you like to send to {contact_name}?")
                    engine.runAndWait()
                    with sr.Microphone() as source:
                        recognizer.adjust_for_ambient_noise(source)
                        audio = recognizer.listen(source)
                        try:
                            message = recognizer.recognize_google(audio)
                            print(f"Message: {message}")
                            send_message(contact_name, message)
                            engine.say("Message sent.")
                            engine.runAndWait()
                        except sr.UnknownValueError:
                            engine.say("Sorry, I couldn't understand the message.")
                            engine.runAndWait()
                elif "make a voice call" in question:
                    engine.say("Please say the contact name.")
                    engine.runAndWait()
                    with sr.Microphone() as source:
                        recognizer.adjust_for_ambient_noise(source)
                        audio = recognizer.listen(source)
                        try:
                            contact_name = recognizer.recognize_google(audio)
                            print(f"Contact name: {contact_name}")
                        except sr.UnknownValueError:
                            engine.say("Sorry, I couldn't understand the contact name.")
                            engine.runAndWait()
                            continue
                    make_audio_call(contact_name)

                elif "make a video call" in question:
                    engine.say("Please say the contact name.")
                    engine.runAndWait()
                    with sr.Microphone() as source:
                        recognizer.adjust_for_ambient_noise(source)
                        audio = recognizer.listen(source)
                        try:
                            contact_name = recognizer.recognize_google(audio)
                            print(f"Contact name: {contact_name}")
                        except sr.UnknownValueError:
                            engine.say("Sorry, I couldn't understand the contact name.")
                            engine.runAndWait()
                            continue
                    make_video_call(contact_name)

                elif "translate" in question:
                    main_for_speech()
                elif "date and time" in question:
                    now = datetime.now()
                    current_time = now.strftime("%Y-%m-%d %H:%M:%S")
                    engine.say("Current Date and Time is" + current_time)
                    engine.runAndWait()
                else:
                    response = respond_to_question(question)
                    if response:
                        engine.say(response)
                        engine.runAndWait()

            except sr.UnknownValueError:
                print("Sorry, I could not understand the audio.")
                engine.say("Sorry, I could not understand that. Could you please repeat?")
                engine.runAndWait()
            except sr.RequestError as e:
                print(f"Could not request results from Google Speech Recognition service; {e}")
                engine.say("I'm having trouble connecting to the speech recognition service.")
                engine.runAndWait()

# Call the authentication function before starting the circles
authenticate_user()

# Start the circle animation in a separate thread
running_animation = True
thread = threading.Thread(target=animate_circles)
thread.daemon = True
thread.start()

greet_user()

# Start listening for questions and responding
listen_and_respond()

# Clean up
pygame.quit()
stream.stop_stream()
stream.close()
p.terminate()
