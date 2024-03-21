from ai_devs import get_task, get_token, send_task
from operator import itemgetter

from langchain.memory import ConversationBufferMemory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from langchain_openai import ChatOpenAI


model = ChatOpenAI()

token = get_token("blogger")
task = get_task(token, True)

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "Jesteś blogerem kuchennym. Twoim zadaniem jest opisać poszczególne etapy wykonywania pizzy Margheritta",
        ),
        MessagesPlaceholder(variable_name="history"),
        ("user", "{input}"),
    ]
)
memory = ConversationBufferMemory(return_messages=True)
chain = (
    RunnablePassthrough.assign(
        history=RunnableLambda(memory.load_memory_variables) | itemgetter("history")
    )
    | prompt
    | model
)

ans = []
for chapter in task["blog"]:
    inputs = {"input": chapter}
    response = chain.invoke(inputs)
    memory.save_context(inputs, {"optput": response.content})
    ans.append(response.content)
    print("# " + chapter)
    print(response.content)

send_task(token, ans)
