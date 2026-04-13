import re
medical_keywords = [
    "fever", "cold", "cough", "headache", "pain", "sore", "throat", "stomach", "vomit",
    "vomiting", "diarrhea", "nausea", "dizzy", "dizziness", "fatigue", "chills", "sweating",
    "rash", "itchy", "itch", "burning", "cramp", "bleeding", "wound", "pus", "swelling",
    "congestion", "runny nose", "sneezing", "breathing", "shortness of breath", "tight chest",
    "palpitations", "blurred vision", "eye pain", "ear pain", "earache", "sensitivity to light",
    "back pain", "neck pain", "leg pain", "knee pain", "arm pain", "muscle pain", "joint pain",
    "chest pain", "abdominal pain", "pelvic pain", "toothache", "gum pain", "jaw pain",
    "infection", "flu", "allergy", "asthma", "diabetes", "hypertension", "cold sore",
    "migraine", "ulcer", "indigestion", "constipation", "acidity", "heartburn", "acne",
    "eczema", "psoriasis", "anxiety", "depression", "insomnia",
    "injury", "cut", "bruise", "fracture", "sprain", "burn", "sting", "bite", "poison", "toxic",
    "baby fever", "child cough", "menstrual", "period pain", "pregnancy", "pregnant", "nipple pain",
    "breast pain", "morning sickness", "spotting", "urine infection", "vaginal itching", "pelvic cramp",
    "gas", "bloating", "kidney pain", "urinary pain", "frequent urination", "urine pain",
    "blood in urine", "stomach ache", "diuretic", "laxative",
    "panic", "fear", "stress", "trauma", "mental", "crying", "can’t sleep", "nightmare",
    "symptom", "diagnosis", "treatment", "medication", "medicine", "remedy", "dose", "prescription",
    "pharmacy", "clinic", "hospital", "sick", "ill", "unwell", "weakness", "soreness", "inflamed"
]
def has_medical_keyword(text: str) -> bool:
    text_lower = text.lower()
    for keyword in medical_keywords:
        if re.search(r'\b' + re.escape(keyword) + r'\b', text_lower):
            return True
    return False
