from openai import OpenAI

client = OpenAI()

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

completion = client.chat.completions.create(
  model="gpt-4o",
  messages=[{"role": "system", "content": "You are a helpful assistant. Use the get_weather tool when the user asks about the weather, otherwise just answer directly."},
            {"role": "user", "content": "What's the weather like in Paris today?"}],
  tools=tools,
)

print(completion)
print(completion.choices[0].message.tool_calls)


completion = client.chat.completions.create(
  model="gpt-4o",
  messages=[{"role": "system", "content": "You are a helpful assistant. Use the get_weather tool when the user asks about the weather, otherwise just answer directly."}, {"role": "user", "content": "Who was the Prime Minister of Britain?"}],
  tools=tools,
)

print(completion)
print(completion.choices[0].message.tool_calls)