from ai_devs import get_task, get_token, send_task

token = get_token("ownapipro")


task = get_task(token, True)

answer = "https://fx1zikyv5a.execute-api.eu-central-1.amazonaws.com/default/ownapipro"
send_task(token, answer)
