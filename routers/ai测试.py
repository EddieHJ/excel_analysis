from openai import OpenAI
import json
import requests

data_example = {
  "data": [
    {
      "event_type_4": "用户操作",
      "count": 44
    },
    {
      "event_type_4": "后台设置",
      "count": 8
    },
    {
      "event_type_4": "咨询",
      "count": 6
    },
    {
      "event_type_4": "代码BUG",
      "count": 2
    }
  ],
  "event_type_3": "WOS"
}


client = OpenAI()


def ai_analyze_data_list(data_list, event_type_3):

    messages = [{
        "role": "user",
        "content": (
            f"以下是 IT 系统中 event_type_3 为 '{event_type_3}' 的事件子类型（event_type_4）和各自的工单数量：\n\n"
            f"{json.dumps(data_list, ensure_ascii=False, indent=2)}\n\n"
            "请总结这些数据的分布情况，指出出现次数最多和最少的事件类型，并用自然语言描述，可适当使用表格或条列。"
        )
    }]

    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=messages
    )

    return completion.choices[0].message.content

# print(ai_analyze_nested(data_example))

# def compare_two_counts(count1: int, count2: int):
#     difference = count1 - count2
#     return difference
#
# client = OpenAI()
#
#
#
# tools = [{
#     "type": "function",
#     "function": {
#         "name": "compare_two_counts",
#         "description": "Describe ",
#         "parameters": {
#             "type": "object",
#             "properties": {
#                 "count1": {"type": "number"},
#                 "count2": {"type": "number"}
#             },
#             "required": ["count1", "count2"],
#             "additionalProperties": False
#         },
#         "strict": True
#     }
# }]
#
# messages = [{"role": "user", "content": "What's the the difference of two numbers, 10 and 20? "
#                                         "Please note it's the service tickets count of 2 weeks, so please analyze the two weeks counts"}]
#
# completion = client.chat.completions.create(
#     model="gpt-4.1",
#     messages=messages,
#     tools=tools,
# )
#
# tool_call = completion.choices[0].message.tool_calls[0]
# args = json.loads(tool_call.function.arguments)
#
# result = compare_two_counts(args["count1"], args["count2"])
#
# messages.append(completion.choices[0].message)  # append model's function call message
# messages.append({                               # append result message
#     "role": "tool",
#     "tool_call_id": tool_call.id,
#     "content": str(result)
# })
#
# completion_2 = client.chat.completions.create(
#     model="gpt-4o-mini-2024-07-18",
#     messages=messages,
#     tools=tools,
# )
#
# print(completion_2.choices[0].message.content)