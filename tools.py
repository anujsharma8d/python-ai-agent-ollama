from datetime import datetime

def get_date_time():
    return datetime.now().strftime("%d/%m/%Y, %H:%M:%S")

TOOLS = [
    {
        "type":"function",
        "function":{
            "name":"get_date_time",
            "description":"Returns the current date and time in formatted string",
            "parameters":{"type":"object","properties":{}}
        }
    }
]

FUNCTION_NAME_TO_FUNCTION_MAP = {
    "get_date_time":get_date_time
}