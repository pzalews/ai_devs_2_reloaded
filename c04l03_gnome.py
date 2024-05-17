from ai_devs import get_task, get_token, send_task
from openai import OpenAI

client = OpenAI()

token = get_token("gnome")


task = get_task(token, True)
question = task["msg"]
url = task["url"]
hint = task["hint"]

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "text", "text": question},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Gfp-wisconsin-madison-the-nature-boardwalk.jpg/2560px-Gfp-wisconsin-madison-the-nature-boardwalk.jpg",
                    },
                },
            ],
        }
    ],
)
print(response.choices[0].message.content)
answer = response.choices[0].message.content
send_task(token, answer)
