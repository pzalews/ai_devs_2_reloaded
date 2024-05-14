import requests
from ai_devs import get_task, get_token, send_task
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

model = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
token = get_token("knowledge")


task = get_task(token, True)
question = task["question"]
link = "https://tasks.aidevs.pl/data/people.json"


prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            'Czy poniższe pytanie dotyczy pieniedzy, kraju czy jest ogólne, odpowiedz jednym słowem "pieniadze" lub "kraj" lub "ogólne"',
        ),
        ("user", question),
    ]
)
chain = prompt | model
response = chain.invoke({})
print(response.content)
answer = response.content
db = []
if answer == "pieniadze":
    link = "http://api.nbp.pl/api/exchangerates/tables/A/"
    response = requests.get(link)
    response.raise_for_status()
    json_data = response.json()
    db = [a["currency"] + " = " + str(a["mid"]) for a in json_data[0]["rates"]]
    # print(db)
if answer == "kraj":
    link = "https://restcountries.com/v3.1/all"
    response = requests.get(link)
    response.raise_for_status()
    json_data = response.json()
    db = [
        "kraj " + a["name"]["common"] + " populacja " + str(a["population"])
        for a in json_data
    ]
    # print(db)

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "Odpowiedz na zadane pytanie krótko, baza widzy:" + "\n".join(db),
        ),
        ("system", "Nie formatuj liczb, powinny zostac podane bez spacji."),
        ("user", question),
    ]
)
chain = prompt | model
response = chain.invoke({})
print(response.content)
answer = response.content

send_task(token, answer)
