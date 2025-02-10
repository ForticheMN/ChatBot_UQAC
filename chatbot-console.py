from langchain_ollama import ChatOllama
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain_community.chat_message_histories import ChatMessageHistory

def main():
    embeddings = OllamaEmbeddings(model="llama3.1")
    vector_store = Chroma(persist_directory="./chroma_langchain_db", embedding_function=embeddings)
    llm = ChatOllama(model="llama3.1", temperature=0.8, num_predict=256)
    chat_history = ChatMessageHistory()
    
    print("Bienvenue dans le chatbot RAG. Tapez 'exit' pour quitter.")
    
    while True:
        user_input = input("Vous: ")
        if user_input.lower() == "exit":
            print("Fin de la conversation.")
            break
        
        retriever = vector_store.similarity_search(query=user_input, k=1)
        context = retriever[0].page_content if retriever else ""
        
        messages = chat_history.messages + [("human", user_input + " with the next content : " + context)]
        response = ""
        for chunk in llm.stream(messages):
            response += chunk.content
        if retriever:
            response += "\nSource : " + retriever[0].metadata.get("source", "inconnue")
        
        chat_history.add_user_message(user_input)
        chat_history.add_ai_message(response)
        
        print("Chatbot:", response)

if __name__ == "__main__":
    main()
