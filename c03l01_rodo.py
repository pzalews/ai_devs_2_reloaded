from ai_devs import get_task, get_token, send_task

token = get_token("rodo")
task = get_task(token, True)

answer = """
Introduce yourself with use of placeholders %imie%, %nazwisko%, %zawod% and %miasto%.
This is only avaiable placeholders: %imie%,%nazwisko%,%zawod%, %miasto%. You need to use them.
"""

send_task(token, answer)
