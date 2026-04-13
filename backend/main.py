from intent_utils import has_medical_keyword
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import torch
from transformers import (
    BertTokenizerFast, BertForSequenceClassification,
    BlenderbotTokenizer, BlenderbotForConditionalGeneration
)
from sentence_transformers import SentenceTransformer
from dosage_recommender import get_dosage

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
emotion_model_path = "emotion_model"
emotion_model = BertForSequenceClassification.from_pretrained(emotion_model_path)
emotion_tokenizer = BertTokenizerFast.from_pretrained(emotion_model_path)
emotion_model.eval()
label_names = ['sadness', 'joy', 'love', 'anger', 'fear', 'surprise']

def predict_emotion(text):
    inputs = emotion_tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    with torch.no_grad():
        logits = emotion_model(**inputs).logits
        predicted_label = torch.argmax(logits, dim=1).item()
        return label_names[predicted_label] if predicted_label < len(label_names) else "undefined"

basic_disease_map = {
    "fever": "Paracetamol", "cold": "Cetirizine", "cough": "Benadryl", "headache": "Crocin",
    "diarrhea": "ORS Sachets", "vomiting": "Ondansetron", "sore throat": "Strepsils",
    "body pain": "Dolo 650", "stomach ache": "Cyclopam", "acidity": "Gelusil", "constipation": "Lactulose",
    "indigestion": "Digene", "allergy": "Levocetirizine", "nausea": "Domperidone", "muscle pain": "Volini",
    "eye infection": "Ciplox Eye Drops", "ear pain": "Otogesic", "skin rash": "Candid B Cream",
    "back pain": "Brufen", "toothache": "Mefkind Forte"
}
import joblib
xgb_model = joblib.load("medication_model/xgboost_drug_model.pkl")
label_encoder = joblib.load("medication_model/label_encoder.pkl")

sbert = SentenceTransformer("all-mpnet-base-v2")

chat_model_path = "chatbot_model"
chat_tokenizer = BlenderbotTokenizer.from_pretrained(chat_model_path)
chat_model = BlenderbotForConditionalGeneration.from_pretrained(chat_model_path)

class Message(BaseModel):
    text: str
    history: list = []

@app.post("/emotion")
def detect_emotion(message: Message):
    emotion = predict_emotion(message.text)
    return {"emotion": emotion}

@app.post("/chat")
def chatbot(message: Message):
    emotion = predict_emotion(message.text)
    text_lower = message.text.lower()

    history = message.history[-2:] if len(message.history) >= 2 else message.history
    prompt = ""
    for turn in history:
        prompt += f"User: {turn['user']}\nBot: {turn['bot']}\n"
    prompt += f"User: {message.text}\nBot:"

    try:
        inputs = chat_tokenizer(prompt, return_tensors="pt", truncation=True, max_length=512)
        reply_ids = chat_model.generate(**inputs, max_length=100)
        bot_reply = chat_tokenizer.decode(reply_ids[0], skip_special_tokens=True)
    except Exception as e:
        bot_reply = "Sorry, I'm unable to respond right now."

    medicine = None
    for symptom, drug in basic_disease_map.items():
        if symptom in text_lower:
            medicine = drug
            break

    if medicine is None and has_medical_keyword(message.text):
        embedding = sbert.encode([message.text])
        pred = xgb_model.predict(embedding)
        medicine = label_encoder.inverse_transform(pred)[0]

    dosage = get_dosage(medicine) if medicine else None

    return {
        "reply": bot_reply,
        "emotion": emotion,
        "medicine": medicine,
        "dosage": dosage
    }