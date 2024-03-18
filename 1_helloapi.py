from ai_devs import get_task, get_token, send_task

token = get_token("helloapi")
task = get_task(token, True)
send_task(token, task["cookie"])
