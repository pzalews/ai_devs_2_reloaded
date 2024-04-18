from ai_devs import get_task, get_token, send_task

token = get_token("functions")
task = get_task(token, True)

answer = {
    "name": "addUser",
    "description": "Adding new user",
    "parameters": {
        "type": "object",
        "properties": {
            "name": {"type": "string", "description": "first name "},
            "surname": {"type": "string", "description": "surname "},
            "year": {"type": "integer", "description": "year of birth "},
        },
    },
}

send_task(token, answer)
