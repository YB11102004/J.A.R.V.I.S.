import smtplib
import ssl
from email.message import EmailMessage
import pyttsx3
import speech_recognition as sr

# Initialize pyttsx3 engine for speech output
engine = pyttsx3.init()

# Initialize the recognizer for voice input
recognizer = sr.Recognizer()

# Capture email details from voice input
def listen_for_input(prompt):
    engine.say(prompt)
    engine.runAndWait()

    with sr.Microphone() as source:
        print(prompt)
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
        
        try:
            print("Recognizing...")
            text = recognizer.recognize_google(audio)
            print(f"You said: {text}")
            return text
        except sr.UnknownValueError:
            engine.say("Sorry, I couldn't understand. Please try again.")
            engine.runAndWait()
            return listen_for_input(prompt)
        except sr.RequestError:
            engine.say("Sorry, the speech service is unavailable. Please try again later.")
            engine.runAndWait()
            return None

def email_details(email_id,password):
    email_sender = email_id
    email_password = password
    email_receiver = listen_for_input("Please say the recipient's email address.")
    email_receiver=email_receiver+'@gmail.com'
    email_receiver = email_receiver.replace(" ", "")
    # Get email subject
    subject = listen_for_input("Please say the subject of your email.")

    # Get email body/content
    body_prompt = "Now please say the body of your email message."
    body = listen_for_input(body_prompt)

    # Create email message object
    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email_receiver
    em['Subject'] = subject
    em.set_content(body)

    # Add SSL (layer of security)
    context = ssl.create_default_context()

    # Log in and send the email
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(email_sender, email_password)
            smtp.sendmail(email_sender, email_receiver, em.as_string())
            print("Mail sent successfully!")
            engine.say("Mail sent successfully!")
            engine.runAndWait()
    except Exception as e:
        print(f"Error: {e}")
        engine.say(f"Sorry, there was an error: {e}")
        engine.runAndWait()
