from openai import OpenAI
import pyttsx3

# https://github.com/marketplace/models/catalog - use this link to set up a new token for the OpenAI GPT-4o model

engine = pyttsx3.init()
def respond_to_question(question):
    question = question.lower()
    client = OpenAI(
        base_url="https://models.inference.ai.azure.com",
        api_key="USE_YOUR_OWN_GITHUB_TOKEN",
    )
    while True:
        if(question=="exit"):
            engine.say("Goodbye! Have Fun!")
            engine.runAndWait()
            break
        response = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "",
                },
                {
                    "role": "user",
                    "content": question,
                }
            ],
            model="gpt-4o",
            temperature=1,
            max_tokens=4096,
            top_p=1
        )
        res=response.choices[0].message.content
        return res
