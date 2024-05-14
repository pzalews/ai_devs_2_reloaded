import json
import requests
from ai_devs import get_task, get_token, send_task
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import Qdrant

model = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
token = get_token("search")


task = get_task(token, True)
question = task["question"]
link = "https://unknow.news/archiwum_aidevs.json"

response = requests.get(link)
response.raise_for_status()
json_data = response.json()

teksts = [a["info"] for a in json_data]
metas = [{"title": a["title"], "url": a["url"]} for a in json_data]

db = Qdrant.from_texts(
    teksts,
    OpenAIEmbeddings(model="text-embedding-3-large"),
    metas,
    location="http://localhost:6333",
)

print(question)
docs = db.similarity_search(question, 1)
print(docs)
answer = docs[0].metadata.get("url")
print(answer)

send_task(token, answer)
