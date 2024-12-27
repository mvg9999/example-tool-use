from openai import OpenAI
import os
import requests
import json


def get_work_orders(business_id, start_date, end_date, fields = ['id', 'jobid', 'status', 'wasFinished']):
    pass

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_work_orders",
            "parameters": {
                "type": "object",
                "properties": {
                    "business_id": {
                        "type": "string"
                    }, 
                    "start_date": {
                        "type": "string"
                    },
                    "end_date": {
                        "type": "string"
                    }, 
                    "fields": {
                        "type": "array",
                        "items": {
                            "type": "string"
                        }
                    }
                },
                "required": ["business_id", "start_date", "end_date", "fields"]
            },
        },
    }
]
def get_weather(location):
    api_key = '7bf332874a874ceca40225826242512'  # Replace with your actual API key
    url = f'http://api.weatherapi.com/v1/current.json?key={api_key}&q={location}'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        res_ =  data['current']
        print("Raw weather output:")
        print(res_)
        return res_
    else:
        return {"error": f"Unable to fetch weather data for {location}"}

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {"type": "string"}
                },
                "required": ["location"]
            },
        },
    }
]

def execute_tool_call(tool_call):
    print("\n")
    print(f"Executing tool call: {tool_call}")
    print(tool_call)
    if tool_call.function.name == "get_weather":
        # Parse the JSON string arguments
        args = json.loads(tool_call.function.arguments)
        location = args["location"]
        result = get_weather(location)
        return result
    return None

def handle_completion_response(completion):
    message = completion.choices[0].message
    
    # Check if there are any tool calls
    if message.tool_calls:
        tool_call_message = message.tool_calls[0]
        tool_result = execute_tool_call(tool_call_message)

        # Create follow-up message with tool results
        messages = [
            {"role": "assistant", "content": None, "tool_calls": [tool_call_message]},
            {"role": "tool", "tool_call_id": tool_call_message.id, "content": str(tool_result)}
        ]
        
        # Get the follow-up response
        follow_up = client.chat.completions.create(
            model="gpt-4o",
            messages=messages
        )
        return follow_up.choices[0].message.content
    else:
        # If no tool calls, return the direct message content
        return message.content

print("=========")
print("Example 1:")
print("\n")
completion = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "system", "content": "You are a helpful assistant. Use the get_weather tool when the user asks about the weather, otherwise just answer directly. If you do use the tool, make sure to add a bit of fun commentary and not just say what the data. "},
              {"role": "user", "content": "What's the weather like in Paris today? Give fun commentary!"}],
    tools=tools,
)

print("Completion object:")
print(completion)
print("\n")
response = handle_completion_response(completion)
print("\n")
print("Response:")
print(response)

print("\n")
print("Example 2:")
completion = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "system", "content": "You are a helpful assistant. Use the get_weather tool when the user asks about the weather, otherwise just answer directly. If you do use the tool, make sure to add a bit of fun commentary and not just say what the data is. "},
              {"role": "user", "content": "Who was the Prime Minister of Britain in 2010?"}],
    tools=tools,
)

response = handle_completion_response(completion)
print(response)
