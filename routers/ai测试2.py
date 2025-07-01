import json
from openai import OpenAI

client = OpenAI()

def analyze_ticket_periods(tickets1: list[dict], tickets2: list[dict]) -> str:
    """
    用于分析两段时间的 IT 工单数据差异，并生成自然语言总结报告。
    参数：
        tickets1: 第一段时间的工单统计数据（event_type_4 + count）
        tickets2: 第二段时间的工单统计数据（event_type_4 + count）
    返回：
        GPT 返回的自然语言分析结果
    """
    prompt = f"""
我有两段时间内的 IT 工单统计数据，结构如下：

第一段时间的数据：
{json.dumps(tickets1, ensure_ascii=False, indent=2)}

第二段时间的数据：
{json.dumps(tickets2, ensure_ascii=False, indent=2)}

每条记录的 event_type_4 是子事件类型，count 是该类型的工单数量。

请你对比这两段时间内的各类事件数量差异，指出：
1. 哪些事件的数量上升了，增加了多少；
2. 哪些事件下降了，减少了多少；
3. 哪些事件是新增的；
4. 哪些事件是消失的；
5. 如果你认为数据变化有趋势或潜在原因，可以尝试分析；

    """.strip()

    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}]
    )

    return completion.choices[0].message.content
