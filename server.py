from fastapi import FastAPI
from pydantic import BaseModel
from transformers import pipeline

# Charger le modèle (ex: BlenderBot ou un autre modèle de chatbot)
chatbot = pipeline("conversational", model="pathtomodel")

# Créer une application FastAPI
app = FastAPI()

# Définir la structure des requêtes
class ChatRequest(BaseModel):
    message: str

# Endpoint pour recevoir un message et répondre
@app.post("/chat")
async def chat(request: ChatRequest):
    response = chatbot(request.message)
    return {"reply": response[0]["generated_text"]}
