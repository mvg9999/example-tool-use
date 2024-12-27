from openai import OpenAI
import os
import requests
import json


def get_business_id_from_name(business_name):
    print(f"\n[DEBUG] get_business_id_from_name called with:\n- business_name: {business_name}")
    result = "100"
    print(f"[DEBUG] Returning business_id: {result}")
    return result

def get_work_orders(business_id, start_date, end_date, fields):
    print(f"\n[DEBUG] get_work_orders called with:\n- business_id: {business_id}\n- start_date: {start_date}\n- end_date: {end_date}\n- fields: {fields}")
    result = []  # or your actual implementation
    print(f"[DEBUG] Returning work_orders: {result}")
    return result

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_work_orders",
            "description": "Get work orders for a business given the business ID, start date, end date, and fields to return. Make sure to use the business ID from the get_business_id_from_name tool if you don't have it.",
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
                            "type": "string",
                            "enum": [
                                "business_id",
                                "business_name",
                                "job_id",
                                "job_location",
                                "job_created",
                                "job_finished",
                                "worker_id"
                            ]
                        }
                    }
                },
                "required": ["business_id", "start_date", "end_date", "fields"]
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_business_id_from_name",
            "description": "Get the business ID from the name of a business. Use this if you don't have the business ID and need to look it up.",
            "parameters": {
                "type": "object",
                "properties": {
                    "business_name": {
                        "type": "string",
                        "description": "The name of the business to look up"
                    }
                },
                "required": ["business_name"]
            },
        },
    }
]

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Example conversation using the tool
messages = []

# System message
messages.append({"role": "system", "content": "You are a helpful assistant that can retrieve work order information"})


print("\n[DEBUG] Initial messages:", json.dumps(messages, indent=2))

# Handle the response
def process_assistant_response(response, messages):
    assistant_message = response.choices[0].message
    print("\n[DEBUG] Assistant message:", json.dumps(assistant_message.model_dump(), indent=2))

    if not assistant_message.tool_calls:
        print("\n[DEBUG] No tool calls - returning final response")
        return assistant_message.content

    for tool_call in assistant_message.tool_calls:
        print(f"\n[DEBUG] Processing tool call: {tool_call.function.name}")
        function_call = tool_call.function
        function_args = json.loads(function_call.arguments)
        print(f"\n[DEBUG] Function arguments parsed:", json.dumps(function_args, indent=2))
        
        # Execute the appropriate function
        if function_call.name == "get_business_id_from_name":
            result = get_business_id_from_name(
                business_name=function_args["business_name"]
            )
        elif function_call.name == "get_work_orders":
            result = get_work_orders(
                business_id=function_args["business_id"],
                start_date=function_args["start_date"],
                end_date=function_args["end_date"],
                fields=function_args["fields"]
            )
        
        # Add the assistant's message and the function result to the conversation
        messages.append(assistant_message.model_dump())
        messages.append({
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": json.dumps(result)
        })
    
    # Make another API call with updated messages
    print("\n[DEBUG] Making follow-up API call...")
    next_response = client.chat.completions.create(
        model="gpt-4-turbo-preview",
        messages=messages,
        tools=tools,
        tool_choice="auto"
    )
    
    # Recursively process the new response
    return process_assistant_response(next_response, messages)

# User message
messages.append({"role": "user", "content": "Get me the work orders for business ABC123 between Jan 1-15 2024. I need the job IDs and locations."})

print("="*100)
print("Example 1:")
# Make the initial API call
print("\n[DEBUG] Making initial API call...")
response = client.chat.completions.create(
    model="gpt-4-turbo-preview",
    messages=messages,
    tools=tools,
    tool_choice="auto"
)

# Process the response chain
final_response = process_assistant_response(response, messages)
print("\n[DEBUG] Final response:", final_response)

print("="*100)
print("Example 2:")

# User message
messages.append({"role": "user", "content": "Write me a haiku about elephants."})

# Make the initial API call
print("\n[DEBUG] Making initial API call...")
response = client.chat.completions.create(
    model="gpt-4-turbo-preview",
    messages=messages,
    tools=tools,
    tool_choice="auto"
)

# Process the response chain
final_response = process_assistant_response(response, messages)
print("\n[DEBUG] Final response:", final_response)
