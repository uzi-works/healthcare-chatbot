#  AI-Powered Healthcare Chatbot

##  Overview

The AI-Powered Healthcare Chatbot is an intelligent system designed to assist users by analyzing their symptoms and emotions to provide relevant medication recommendations and responses. The system integrates Natural Language Processing (NLP), Machine Learning (ML), and conversational AI to deliver a smart healthcare assistance experience.

---

##  Problem Statement

Patients often struggle to identify appropriate medication or understand their symptoms without consulting a doctor. Additionally, emotional state plays a crucial role in health, which is often ignored by traditional systems.

---

##  Solution

This project combines:

* Emotion detection using NLP
* Medication recommendation system
* Conversational chatbot interface

to provide a more personalized and intelligent healthcare assistant.

---

##  Key Features

*  Chatbot-based interaction
*  Emotion detection from user input
*  Medication recommendation system
*  Rule-based fallback mechanism
*  Machine Learning-based predictions
*  Cleaned and preprocessed medical dataset

---

## Tech Stack

* **Programming Language:** Python
* **Machine Learning:** Scikit-learn, XGBoost
* **NLP Models:** BERT, SBERT, BlenderBot
* **Frontend (Planned/Optional):** Streamlit / Web UI
* **Dataset:** UCI Healthcare Dataset

---

##  System Architecture

1. User inputs symptoms or message
2. Emotion Detection Model analyzes sentiment
3. Medication Recommendation Model suggests medicines
4. Chatbot (BlenderBot) generates response
5. Rule-based system handles edge cases

---

##  Project Structure

healthcare-chatbot/
│
├── data/                      # Dataset files
├── models/                    # Trained ML/NLP models
├── preprocessing/             # Data cleaning scripts
├── emotion_model/             # Emotion detection module
├── recommendation_model/      # Medication recommendation module
├── chatbot/                   # Chatbot integration
├── app.py                     # Main application file
└── README.md

---

##  How to Run the Project

### 1️ Clone the repository

git clone https://github.com/uzi-works/healthcare-chatbot
cd healthcare-chatbot

### 2️ Install dependencies

pip install -r requirements.txt

### 3️ Run the application

python app.py

---

##  Dataset Details

* Source: UCI Health Repository
* Total Instances: 161,212
* Features:

  * cleaned_review
  * cleaned_condition

---

##  Current Performance

* Model Accuracy: ~50% (ongoing improvements)
* Scope for improvement with better dataset and tuning

---

##  Future Improvements

* Improve model accuracy using advanced deep learning models
* Deploy as a web application
* Integrate real-time doctor consultation
* Add multilingual support
* Enhance UI/UX

---

##  Screenshots

<img width="888" height="562" alt="image" src="https://github.com/user-attachments/assets/606def8b-008e-49ba-97a3-b8ec469bb670" />
<img width="831" height="797" alt="Screenshot 2026-04-13 200320" src="https://github.com/user-attachments/assets/82f691e0-0c4c-418b-8cba-d6baedfe2c8c" />
<img width="750" height="718" alt="Screenshot 2026-04-13 200344" src="https://github.com/user-attachments/assets/6d56a595-f074-4941-95f9-01441cda25f7" />
<img width="752" height="719" alt="Screenshot 2026-04-13 200350" src="https://github.com/user-attachments/assets/a28b3c45-0428-46ec-a7e4-649573334ade" />

---


##  Contributing

Contributions are welcome! Feel free to fork this repository and submit a pull request.

---

##  License

This project is open-source and available under the MIT License.

---

##  Author

**Uzair Sabir**
B.Tech CSE | AI Enthusiast

---

##  Acknowledgements

* UCI Machine Learning Repository
* Open-source NLP models and libraries
