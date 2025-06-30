from openai import OpenAI
import json
import requests

def compare_two_counts(count1: int, count2: int):
    difference = count1 - count2
    return difference

client = OpenAI()

tools = [{
    "type": "function",
    "function": {
        "name": "compare_two_counts",
        "description": "Describe ",
        "parameters": {
            "type": "object",
            "properties": {
                "count1": {"type": "number"},
                "count2": {"type": "number"}
            },
            "required": ["count1", "count2"],
            "additionalProperties": False
        },
        "strict": True
    }
}]

messages = [{"role": "user", "content": "What's the the difference of two numbers, 10 and 20? "
                                        "Please note it's the service tickets count of 2 weeks, so please analyze the two weeks counts"}]

completion = client.chat.completions.create(
    model="gpt-4.1",
    messages=messages,
    tools=tools,
)

tool_call = completion.choices[0].message.tool_calls[0]
args = json.loads(tool_call.function.arguments)

result = compare_two_counts(args["count1"], args["count2"])

messages.append(completion.choices[0].message)  # append model's function call message
messages.append({                               # append result message
    "role": "tool",
    "tool_call_id": tool_call.id,
    "content": str(result)
})

completion_2 = client.chat.completions.create(
    model="gpt-4o-mini-2024-07-18",
    messages=messages,
    tools=tools,
)

print(completion_2.choices[0].message.content)