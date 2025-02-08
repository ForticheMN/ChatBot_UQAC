import streamlit as st
from transformers import pipeline

# Charger le modèle (ex: BlenderBot ou autre)
chatbot = pipeline("conversational", model="facebook/blenderbot-400M-distill")

# Interface utilisateur avec Streamlit
st.title("Chatbot IA 🤖")

# Stocker l'historique des messages
if "messages" not in st.session_state:
    st.session_state.messages = []

# Afficher les messages précédents
for msg in st.session_state.messages:
    role = "👤" if msg["from"] == "user" else "🤖"
    st.text(f"{role} {msg['text']}")

# Champ d'entrée utilisateur
user_input = st.text_input("Votre message :", "")

if user_input:
    # Ajouter le message utilisateur
    st.session_state.messages.append({"text": user_input, "from": "user"})

    # Obtenir la réponse du chatbot
    response = chatbot(user_input)
    bot_reply = response[0]["generated_text"]

    # Ajouter la réponse du bot
    st.session_state.messages.append({"text": bot_reply, "from": "bot"})

    # Rafraîchir la page pour afficher les nouveaux messages
    st.rerun()
