import requests
from ai_devs import get_task, get_token, send_task
from time import sleep
from pprint import pprint
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI


max_retries = 3
retry_delay = 5  # seconds
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, sdch",
    "Accept-Language": "en-US,en;q=0.8",
}

token = get_token("scraper")
task = get_task(token, True)
link = task["input"]
print(link)

content = b""
for retry_count in range(max_retries):
    try:
        response = requests.get(link, headers=headers, timeout=25)
        response.raise_for_status()  # Raise an exception for non-2xx status codes
        content = response.content
        break  # Exit the loop if the request was successful
    except requests.exceptions.HTTPError as e:
        print(f"HTTP error occurred (attempt {retry_count+1}/{max_retries}): {e}")
        if retry_count < max_retries - 1:
            print(f"Retrying in {retry_delay} seconds...")
            sleep(retry_delay)
        else:
            print("Maximum number of retries reached. Exiting.")
            exit(1)
    except requests.exceptions.Timeout as e:
        print(f"Timeout (attempt {retry_count+1}/{max_retries}): {e}")
    except requests.exceptions.ConnectionError as e:
        print(f"Timeout (attempt {retry_count+1}/{max_retries}): {e}")

print(content)

question = task["question"]

model = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
# What is a name in question
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", content.decode()),
        ("user", "Odpowiedz krotko na ponizsze pytanie: {input}"),
    ]
)
chain = prompt | model
response = chain.invoke({"input": question})
print(response.content)

answer = response.content

send_task(token, answer)
