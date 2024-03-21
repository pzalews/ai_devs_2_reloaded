from ai_devs import get_task, get_token, send_task
from openai import OpenAI

client = OpenAI()

token = get_token("blogger")
task = get_task(token, True)

ans = []
for chapter in task["blog"]:
    m = [
        {
            "role": "system",
            "content": "Jesteś blogerem kuchennym. Twoim zadaniem jest opisać poszczególne etapy wykonywania pizzy Margheritta",
        },
    ]
    for a in ans:
        m.append({"role": "user", "content": a[0]})
        m.append({"role": "assistant", "content": a[1]})
    m.append(
        {"role": "user", "content": chapter},
    )
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=m,
    )
    print("# " + chapter)
    print(response.choices[0].message.content)
    ans.append(response.choices[0].message.content)


send_task(token, ans)
