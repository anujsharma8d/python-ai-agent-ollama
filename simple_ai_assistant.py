import os


from openai import OpenAI
from dotenv import load_dotenv
from types import SimpleNamespace


from tools import TOOLS,run_tool
from Utilities.utilities import log


load_dotenv()


client = OpenAI(
    base_url= os.getenv("BASE_URL"),
    api_key= os.getenv("API_KEY")
)

messages = []

messages.append(
    {
        "role":"system",
        "content":"Act as a very humble agent and respond with 1000 words"
    }
)

MAX_STEPS = 5

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

    def build_tool_calls_payload(call_list):
        payload = []

        for tool_call in call_list:
            tool_call_dict={
                "id":tool_call.id,
                "type":"function",
                "function":{
                    "name":tool_call.function.name,
                    "arguments":tool_call.function.arguments
                }
            }
            payload.append(tool_call_dict)

        return payload

    for step in range(MAX_STEPS):

        try:

            stream = client.chat.completions.create(
                model=os.getenv("MODEL"),
                messages=messages,
                tools=TOOLS,
                stream=True
            )
            
            full_response = ""
            calls = {}
            showed = False

            for chunk in stream:
                if not chunk.choices:
                    continue 

                delta= chunk.choices[0].delta
                if(delta.content):
                    if not showed:
                        print("Assistant: "+ delta.content, end= "",flush=True)
                        showed = True
                    else:
                        print(delta.content, end= "",flush=True)
                    
                    full_response+=delta.content


                for tool_call in (delta.tool_calls or []):
                    obj = calls.setdefault(tool_call.index, SimpleNamespace(id=None ,function = SimpleNamespace(name="",arguments="") ))
                    if(tool_call.id):
                        obj.id = tool_call.id
                    if(tool_call.function and tool_call.function.name):
                        obj.function.name += tool_call.function.name
                    if(tool_call.function and tool_call.function.arguments):
                        obj.function.arguments += tool_call.function.arguments

            if(showed):
                print()

            call_list = []
            for key in sorted(calls):
                call_list.append(calls[key])

            messages.append(
                {
                    "role":"assistant",
                    "content":full_response,
                    "tool_calls":build_tool_calls_payload(call_list)
                }
            )

            for tool_call in call_list:
                result = run_tool(tool_call)

                messages.append({
                    "role":"tool",
                    "tool_call_id":tool_call.id,
                    "content":str(result)
                })
                

            log(f"Step {step+1}: model requested {len(call_list)} tool calls")
            
            if not call_list:
                break

        except KeyboardInterrupt:
            print()
            print("{  Stopped by You  }")
            break


    else:
        fallback = "Sorry, I couldn't finish this within the step limit"

        messages.append(
            {
                "role":"assistant",
                "content":fallback
            }
        )

        print("Assistant: " + fallback)
        continue
        
