import requests, json
from ai_devs import get_task, get_token, send_task
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

model = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
token = get_token("tools")


task = get_task(token, True)
question = task["question"]
example1 = task["example for ToDo"]
exmaple2 = task["example for Calendar"]
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            'Czy poniższe zdanie posiada konkretna datę? Jeżeli tak zwróć obiekt json "tool":"Calendar","desc":"Opis wydarzenia","date":"2024-05-15"'
            + 'Jeżeli nie zwróć obiekt json "tool":"ToDo","desc":"Treść zadania" '
            + "Przykład: "
            + 'Przypomnij mi, że mam kupić mleko = "tool":"ToDo","desc":"Kup mleko" '
            + 'Jutro mam spotkanie z Marianem = "tool":"Calendar","desc":"Spotkanie z Marianem","date":"2024-05-15"',
        ),
        (
            "system",
            "Dzisiaj jest wtorek 2024-05-14. Zawsze używaj daty w formacie YYYY-MM-DD",
        ),
        ("user", question),
    ]
)
chain = prompt | model
response = chain.invoke({})
print(response.content)
answer = json.loads(response.content)
send_task(token, answer)
