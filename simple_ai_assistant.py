from openai import OpenAI
from dotenv import load_dotenv
import os
from tools import TOOLS,FUNCTION_NAME_TO_FUNCTION_MAP
import json

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
        messages=messages,
        tools=TOOLS
    )

    msg = response.choices[0].message

    if(msg.tool_calls):
        messages.append(msg)

        for tool_call in msg.tool_calls:
            func_name = tool_call.function.name
            args_name = json.loads(tool_call.function.arguments)

            fn = FUNCTION_NAME_TO_FUNCTION_MAP[func_name]
            result = fn(**args_name)

            messages.append({
                "role":"tool",
                "tool_id":tool_call.id,
                "content":str(result)
            })

        response = client.chat.completions.create(
            model=os.getenv("MODEL"),
            messages=messages,
        )

        msg = response.choices[0].message

    messages.append(
        {
            "role":"assistant",
            "content":msg.content
        }
    )

    print(response.choices[0].message.content)