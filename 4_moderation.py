from ai_devs import get_task, get_token, send_task
from openai import OpenAI

client = OpenAI()

token = get_token("moderation")
task = get_task(token, True)

ans = client.moderations.create(input=task["input"], model="text-moderation-latest")

send_task(token, [int(x.flagged) for x in ans.results])
