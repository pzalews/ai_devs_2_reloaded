from ai_devs import get_task, get_token, send_task
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

token = get_token("inprompt")
task = get_task(token, True)

input = task["input"]
question = task["question"]

model = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
# What is a name in question
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            You need to return the first name of person that is in sentence below.
            Example:
            "Alice jest gamon" => "Alice"
            "Mateusz lubi pizze" => "Mateusz"
            "Jakiego koloru Adam ma włosy?" => "Adam"
            """,
        ),
        ("user", "{input}"),
    ]
)
chain = prompt | model
response = chain.invoke({"input": question})
print(response.content)

# Fileter database
input_filtered = [s for s in input if response.content in s]

# Answer question
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "Odpowiedź na zadane pytanie bazując na wiedzy: "
            + "\n".join(input_filtered),
        ),
        ("user", "{input}"),
    ]
)
chain = prompt | model
response = chain.invoke({"input": question})
send_task(token, response.content)
