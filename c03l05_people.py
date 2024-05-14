import json
import requests
from ai_devs import get_task, get_token, send_task
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import Qdrant

model = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
token = get_token("people")


task = get_task(token, True)
question = task["question"]
link = "https://tasks.aidevs.pl/data/people.json"

response = requests.get(link)
response.raise_for_status()
json_data = response.json()

teksts = [
    a["imie"]
    + " "
    + a["nazwisko"]
    + ": ulubiony kolor to "
    + a["ulubiony_kolor"]
    + " "
    + a["o_mnie"]
    for a in json_data
]
metas = [{"imie": a["imie"], "nazwisko": a["nazwisko"]} for a in json_data]

db = Qdrant.from_texts(
    teksts,
    OpenAIEmbeddings(model="text-embedding-3-large"),
    metas,
    location="http://localhost:6333",
)

print(question)
docs = db.similarity_search(question, 1)
print(docs)
answer = docs[0].page_content
print(answer)

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "Baza danych:" + "\n".join([d.page_content for d in docs]),
        ),
        ("user", question),
    ]
)
chain = prompt | model
response = chain.invoke({})
print(response.content)
answer = response.content

send_task(token, answer)
