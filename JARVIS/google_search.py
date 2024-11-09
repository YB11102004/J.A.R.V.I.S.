import webbrowser
import pyttsx3
from googlesearch import search  # Importing the googlesearch module

# Initialize the text-to-speech engine
engine = pyttsx3.init()

def speak(message):
    """Speaks a given message using TTS."""
    engine.say(message)
    engine.runAndWait()

def open_google():
    """Opens the Google homepage."""
    url = "https://www.google.com"
    webbrowser.open(url)
    speak("Opening Google.")

def search_google(query, num_results=5, open_top_result=False):
    speak(f"Searching Google for {query}. Here are the top results:")

    # Fetching the search results
    results = list(search(query, num_results=num_results))
    for i, url in enumerate(results, start=1):
        print(f"Result {i}: {url}")
    
    # Optionally open the top result in the browser
    if open_top_result and results:
        webbrowser.open(results[0])
        speak("Opening the top result.")
    else:
        speak("These are the top results. You can open any one as needed.")