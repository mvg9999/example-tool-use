from openai import OpenAI
import os

import requests

def get_weather(location):
    api_key = 'YOUR_API_KEY'  # Replace with your actual API key
    url = f'http://api.weatherapi.com/v1/current.json?key={7bf332874a874ceca40225826242512}&q={location}'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data['current']
    else:
        return None


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
          },
      },
  }
]
print("\n\n\n")
print("=========")
print("Example 1:")
completion = client.chat.completions.create(
  model="gpt-4o",
  messages=[{"role": "system", "content": "You are a helpful assistant. Use the get_weather tool when the user asks about the weather, otherwise just answer directly."},
            {"role": "user", "content": "What's the weather like in Paris today?"}],
  tools=tools,
)

print(completion)
print(completion.choices[0].message.tool_calls)

print("\n\n\n")
print("Example 2:")
completion = client.chat.completions.create(
  model="gpt-4o",
  messages=[{"role": "system", "content": "You are a helpful assistant. Use the get_weather tool when the user asks about the weather, otherwise just answer directly."}, {"role": "user", "content": "Who was the Prime Minister of Britain?"}],
  tools=tools,
)

print(completion)
print(completion.choices[0].message.tool_calls)