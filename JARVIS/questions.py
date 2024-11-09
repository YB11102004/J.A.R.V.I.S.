import pyttsx3

# Initialize the text-to-speech engine
engine = pyttsx3.init()

def respond_to_question(question):
    """
    Responds to basic human questions based on predefined responses.
    
    :param question: The question asked by the user
    """
    responses = {
        "how are you": "I'm just a program, but I'm functioning as expected! How can I assist you today?",
        "what is your name": "I'm Jarvis, your personal assistant.",
        "what can you do": "I can assist you with various tasks, including opening applications, answering questions, and more.",
        "tell me a joke": "Why did the scarecrow win an award? Because he was outstanding in his field!",
        "what is the time": "I can't tell the time directly, but you can check your device's clock.",
        "who created you": "I was created by a developer who wanted to have an intelligent assistant."
    }
    
    # Normalize the question to lowercase for easier matching
    question = question.lower()

    # Check if the question is in the predefined responses
    if question in responses:
        answer = responses[question]
        print(answer)  # Print the answer to the console for debugging
        engine.say(answer)  # Use TTS to respond
        engine.runAndWait()
    else:
        default_response = "I'm sorry, I don't have an answer for that."
        print(default_response)
        engine.say(default_response)
        engine.runAndWait()
