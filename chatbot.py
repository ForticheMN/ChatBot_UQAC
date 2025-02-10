from langchain_ollama import ChatOllama
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
# from langchain.memory import ChatMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory

embeddings = OllamaEmbeddings(
    model="llama3.1",
)

vector_store = Chroma(
    persist_directory="./chroma_langchain_db",
    embedding_function=embeddings
)

llm = ChatOllama(
    model = "llama3.1",
    temperature = 0.8,
    num_predict = 256,
)


demo_ephemeral_chat_history = ChatMessageHistory()

question = "Qu'est-ce qu'une personne morale ?"

retriever = vector_store.similarity_search(
    query=question,
    k=1
)

messages = [
    ("human", question + " with the next content : " + retriever[0].page_content),
]

# for chunk in llm.stream(messages):
#     print(chunk.content, end="")
# print("source : " + retriever[0].metadata["source"])

response = ""
for chunk in llm.stream(messages):
    response += chunk.content
response += "source : " + retriever[0].metadata["source"]

demo_ephemeral_chat_history.add_user_message(messages[0][1])

demo_ephemeral_chat_history.add_ai_message(response)

demo_ephemeral_chat_history.messages

input2 = "What did I just ask you?"

demo_ephemeral_chat_history.add_user_message(input2)

demo_ephemeral_chat_history.add_user_message(input2)

response2 = ""
for chunk in llm.stream(demo_ephemeral_chat_history.messages):
    response2 += chunk.content
response2 += "source : " + retriever[0].metadata["source"]

demo_ephemeral_chat_history.add_ai_message(response2)

print(demo_ephemeral_chat_history.messages)
