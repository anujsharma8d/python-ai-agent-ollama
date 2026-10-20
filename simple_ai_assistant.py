from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()


client = OpenAI(
    base_url= os.getenv("BASE_URL"),
    api_key= os.getenv("API_KEY")
)

messages = []

messages.append(
    {
        "role":"system",
        "content":"Act as a very humble agent and respond within 100 words"
    }
)

while True:
    user_input=input("\nYou: ")

    if user_input.lower() in ["bye","exit","goodbye","quit"]:
        break

    messages.append(
        {
            "role":"user",
            "content":user_input
        }
    )

    response = client.chat.completions.create(
        model=os.getenv("MODEL"),
        messages=messages
    )

    messages.append(
        {
            "role":"assistant",
            "content":response.choices[0].message.content
        }
    )

    print(response.choices[0].message.content)