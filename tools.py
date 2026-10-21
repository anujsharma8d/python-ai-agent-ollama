import requests
import json


from datetime import datetime


from Utilities.utilities import log


def get_date_time():
    return datetime.now().strftime("%d/%m/%Y, %H:%M:%S")

def get_city_weather(city):
    url = f"https://wttr.in/{city}?format=3"
    res = requests.get(url,timeout=10)
    res.raise_for_status()
    return res.text

def get_current_location():
    url = "http://ip-api.com/json/"
    res = requests.get(url,timeout=10)
    res.raise_for_status()
    data = res.json()
    return data

TOOLS = [
    {
        "type":"function",
        "function":{
            "name":"get_date_time",
            "description":"Returns the current date and time in formatted string",
            "parameters":{"type":"object","properties":{}}
        }
    },
    {
        "type":"function",
        "function":{
            "name":"get_city_weather",
            "description":"Return the current weather of the provided city",
            "parameters":{
                "type":"object",
                "properties":{
                    "city":{
                        "type":"string",
                        "description":"The city whose weather is needed"
                    }
                },
                "required":["city"]
            }
        }
    },
    {
            "type":"function",
            "function":{
                "name":"get_current_location",
                "description":"Returns the current city of the user",
                "parameters":{"type":"object","properties":{}}
            }
        },
]

FUNCTION_NAME_TO_FUNCTION_MAP = {
    "get_date_time":get_date_time,
    "get_city_weather":get_city_weather,
    "get_current_location":get_current_location,
}

def run_tool(tool_call):
    func_name = tool_call.function.name
    func_args = {}
    
    try:
        func_args = json.loads(tool_call.function.arguments or "{}")
    
        log(f"🔧 {func_name}({func_args})")
    
        fn = FUNCTION_NAME_TO_FUNCTION_MAP[func_name]
        result = fn(**func_args)
    
    
    except Exception as e:
        result = f"Error while running {func_name}:{e}"
        
    log(f"   => {result}")

    return result