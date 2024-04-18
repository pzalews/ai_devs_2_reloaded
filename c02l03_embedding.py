from ai_devs import get_task, get_token, send_task
from langchain_openai import OpenAIEmbeddings

token = get_token("embedding")
task = get_task(token, True)

input = "Hawaiian pizza"


# Set your OpenAI API key

# Create the OpenAIEmbeddings instance
embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")

# Embed a single query
query_embedding = embeddings.embed_query(input)
# print(query_embedding)
print(len(query_embedding))

send_task(token, query_embedding)
