import requests
from ai_devs import get_task, get_token, send_task
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI


model = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
token = get_token("whoami")

hints = []
DONT_KNOW = True

answer = ""
while DONT_KNOW:
    task = get_task(token, True)
    hint = task["hint"]
    hints.append(task["hint"])

    # What is a name in question
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "Dostaniesz fragment historii o konkretnej bardzo znanej osobie. "
                + "\n".join(hints),
            ),
            (
                "user",
                "Podaj imie i nazwisko tej osoby,  jeżeli nie wiesz napisz tylko NIE WIEM ",
            ),
        ]
    )
    chain = prompt | model
    response = chain.invoke({})
    print(response.content)
    answer = response.content
    if "NIE WIEM" not in answer:
        DONT_KNOW = False

send_task(token, answer)
