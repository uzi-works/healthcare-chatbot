import streamlit as st
import torch
import joblib
from transformers import BertTokenizerFast, BertForSequenceClassification, BlenderbotTokenizer, BlenderbotForConditionalGeneration
from sentence_transformers import SentenceTransformer

# ---------- Load Models ----------
@st.cache_resource
def load_models():
    # Load emotion model
    emotion_path = "models/emotion_model"
    emotion_model = BertForSequenceClassification.from_pretrained(emotion_path)
    emotion_tokenizer = BertTokenizerFast.from_pretrained(emotion_path)

    # Load med model
    med_model = joblib.load("models/med_model/xgboost_drug_model.pkl")
    label_encoder = joblib.load("models/med_model/label_encoder.pkl")

    # Load chatbot
    chat_model = BlenderbotForConditionalGeneration.from_pretrained("models/chatbot_model")
    chat_tokenizer = BlenderbotTokenizer.from_pretrained("models/chatbot_model")

    return emotion_model, emotion_tokenizer, med_model, label_encoder, chat_model, chat_tokenizer

emotion_model, emotion_tokenizer, med_model, label_encoder, chat_model, chat_tokenizer = load_models()
sbert = SentenceTransformer("all-mpnet-base-v2")

symptom_map = {
    "fever": "Paracetamol", "cold": "Cetirizine", "cough": "Benadryl", "headache": "Crocin",
    "diarrhea": "ORS Sachets", "vomiting": "Ondansetron", "sore throat": "Strepsils",
    "body pain": "Dolo 650", "stomach ache": "Cyclopam", "acidity": "Gelusil", "constipation": "Lactulose",
    "indigestion": "Digene", "allergy": "Levocetirizine", "nausea": "Domperidone", "muscle pain": "Volini",
    "eye infection": "Ciplox Eye Drops", "ear pain": "Otogesic", "skin rash": "Candid B Cream",
    "back pain": "Brufen", "toothache": "Mefkind Forte"
}

# ---------- Functions ----------
def predict_emotion(text):
    inputs = emotion_tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    with torch.no_grad():
        outputs = emotion_model(**inputs)
        pred = torch.argmax(outputs.logits, dim=1).item()
    return ['sadness', 'joy', 'love', 'anger', 'fear', 'surprise'][pred]

def recommend_medicine(text):
    text = text.lower()
    for key in symptom_map:
        if key in text:
            return symptom_map[key]
    return None

def generate_response(user_input, history):
    emotion = predict_emotion(user_input)
    medicine = recommend_medicine(user_input)

    prompt = ""
    for user, bot in history:
        prompt += f"User: {user}\nBot: {bot}\n"

    prompt += f"User: {user_input}\n"
    prompt += f"I'm feeling {emotion}. I've been experiencing symptoms like: {user_input}."
    if medicine:
        prompt += f" A suitable medicine might be {medicine}."
    prompt += " What can I do?\nBot:"

    try:
        inputs = chat_tokenizer(prompt, return_tensors='pt', truncation=True, max_length=512)
        outputs = chat_model.generate(**inputs, max_length=100)
        bot_reply = chat_tokenizer.decode(outputs[0], skip_special_tokens=True)
    except:
        bot_reply = "I'm having trouble responding right now."

    return bot_reply, emotion, medicine

# ---------- Streamlit UI ----------
st.set_page_config(page_title="Healthcare Chatbot", layout="centered")
st.title("💬 Smart Healthcare Chatbot")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

with st.form("chat_form"):
    user_input = st.text_input("Describe your symptoms or feelings:")
    submitted = st.form_submit_button("Send")

if submitted and user_input:
    response, emotion, medicine = generate_response(user_input, st.session_state.chat_history)
    st.session_state.chat_history.append((user_input, response))
    st.success(f"🧠 Emotion: **{emotion}**")
    if medicine:
        st.info(f"💊 Recommended Medicine: **{medicine}**")

# Display chat history
for i, (user, bot) in enumerate(reversed(st.session_state.chat_history)):
    st.markdown(f"""
    <div style='background:#000000;padding:10px;border-radius:10px;margin-bottom:10px'>
    <b>👤 You:</b> {user}<br>
    <b>🤖 Bot:</b> {bot}
    </div>
    """, unsafe_allow_html=True)
