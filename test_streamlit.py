import streamlit as st
from langchain_ollama import ChatOllama
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain_community.chat_message_histories import ChatMessageHistory

# ✅ Forcer la réinitialisation au démarrage
# if "chat_history" not in st.session_state or st.session_state.get("reset_chat", False):
#     st.session_state.chat_history = ChatMessageHistory()
#     st.session_state.reset_chat = False  # Désactiver la réinitialisation après l'avoir appliquée

# Initialisation des composants
embeddings = OllamaEmbeddings(model="llama3.1")
vector_store = Chroma(persist_directory="./chroma_langchain_db", embedding_function=embeddings)
llm = ChatOllama(model="llama3.1", temperature=0.8, num_predict=256)

# Interface Streamlit
st.title("Chatbot RAG 🤖")
st.session_state.chat_history = ChatMessageHistory()

# ✅ Bouton pour réinitialiser le chat
# if st.button("🔄 Réinitialiser le Chat"):
#     st.session_state.reset_chat = True
#     st.rerun()

# 📌 Affichage de l'historique sous forme de chat
# for msg in st.session_state.chat_history.messages:
#     role = "user" if msg.type == "human" else "assistant"
#     with st.chat_message(role):
#         st.markdown(msg.content)

# ✅ Champ de saisie pour entrer une question
user_input = st.chat_input("Posez votre question...")

# ✅ Traitement du message lorsqu'on envoie une question
if user_input:
    # Ajouter le message utilisateur
    st.session_state.chat_history.add_user_message(user_input)

    # Afficher immédiatement le message utilisateur
    with st.chat_message("user"):
        st.markdown(user_input)

    # Récupérer le contexte depuis ChromaDB
    retriever = vector_store.similarity_search(query=user_input, k=1)
    context = retriever[0].page_content if retriever else ""

    # Construire la requête pour le chatbot
    messages = st.session_state.chat_history.messages + [("human", user_input + " with the next content : " + context)]

    # Générer la réponse du chatbot
    response = ""
    for chunk in llm.stream(messages):
        response += chunk.content

    # Ajouter la source si disponible
    if retriever:
        response += "\n📌 **Source** : " + retriever[0].metadata.get("source", "inconnue")    

    # Ajouter la réponse à l'historique
    st.session_state.chat_history.add_ai_message(response)

    # Afficher immédiatement la réponse du chatbot
    with st.chat_message("assistant"):
        st.markdown(response)
