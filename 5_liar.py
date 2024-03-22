import requests
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from ai_devs import get_task, get_token, send_task

model = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

token = get_token("liar")
task = get_task(token, True)


def get_answer(token, debug=False):
    url = "https://tasks.aidevs.pl/task/" + token
    response = requests.post(url, data={"question": "What is capital city of Poland?"})
    response.raise_for_status()
    if debug:
        print(response.json())
    return response.json()


answer = get_answer(token, True)
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are working as a censor system. 
Please check if this sentence is answer to question about capital city of Poland.
Answer only YES or NO.
            """,
        ),
        ("user", "{input}"),
    ]
)
chain = prompt | model
response = chain.invoke({"input": answer["answer"]})
print(response.content)

send_task(token, response.content)
