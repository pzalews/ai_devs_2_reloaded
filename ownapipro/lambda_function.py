import json
from openai import OpenAI
import boto3

client = OpenAI()

print("Loading function")
# client = boto3.client("dynamodb")
dynamodb = boto3.resource("dynamodb")
tableName = "ownapipro2"
table = dynamodb.Table(tableName)


def respond(err, res=None):
    return {
        "statusCode": "400" if err else "200",
        "body": err.message if err else json.dumps(res),
        "headers": {
            "Content-Type": "application/json",
        },
    }


def ask_chat(question):
    body = table.scan()
    prompt = [{"role": "system", "content": "Odpowiedz krótko na zadane pytanie."}]
    for i in body["Items"]:
        prompt.append({"role": "user", "content": i["id"]})
    prompt.append({"role": "user", "content": question})
    model = client.chat.completions.create(
        model="gpt-4o",
        messages=prompt,
        temperature=0,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )

    response = model.choices[0].message
    table.put_item(Item={"id": question})
    return response.content


def lambda_handler(event, context):
    # print("Received event: " + json.dumps(event, indent=2))

    operation = event["httpMethod"]
    if operation in ["GET", "POST"]:
        payload = (
            event["queryStringParameters"]
            if operation == "GET"
            else json.loads(event["body"])
        )
        response = {}
        response["reply"] = ask_chat(payload["question"])
        return respond(None, response)
    else:
        return respond(ValueError('Unsupported method "{}"'.format(operation)))
