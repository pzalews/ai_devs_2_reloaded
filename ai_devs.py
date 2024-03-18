import requests
import json
import os


def get_token(task):
    url = "https://tasks.aidevs.pl/token/" + task
    data = {"apikey": os.getenv("AI_DEVS_CODE")}
    response = requests.post(
        url, data=json.dumps(data), headers={"Content-Type": "application/json"}
    )
    response.raise_for_status()
    return response.json().get("token")


def get_task(token, debug=False):
    url = "https://tasks.aidevs.pl/task/" + token
    response = requests.get(url, headers={"Content-Type": "application/json"})
    response.raise_for_status()
    if debug:
        print(response.json())
    return response.json()


def send_task(token, answer):
    url = "https://tasks.aidevs.pl/answer/" + token
    data = {"answer": answer}
    json_data = json.dumps(data)
    response = requests.post(
        url, data=json_data, headers={"Content-Type": "application/json"}
    )
    response.raise_for_status()
    print(response.json())
