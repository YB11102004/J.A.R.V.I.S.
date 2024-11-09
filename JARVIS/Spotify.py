import pyautogui
import os
import time
import pyttsx3

engine = pyttsx3.init()
def search_song(song_name):
    pyautogui.hotkey('ctrl','l')
    pyautogui.write(song_name,interval=0.1)
    engine.say(f'Playing the song {song_name}')
    engine.runAndWait()
    for key in ['enter','pagedown','tab','tab','enter','enter']:
        time.sleep(2)
        pyautogui.press(key)

def pause_song():
    pyautogui.press('space')
    engine.say("Song paused")
    engine.runAndWait()

def play_song():
    pyautogui.press('space')
    engine.say("Resuming song")
    engine.runAndWait()