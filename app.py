# app.py

import streamlit as st
import pickle
import re
import string

# -----------------------------
# PAGE CONFIG (Dark Style)
# -----------------------------
st.set_page_config(
    page_title="Spam Detector",
    page_icon="📧",
    layout="centered"
)

# Custom Dark CSS
st.markdown("""
<style>
body {
    background-color: #0e1117;
}
.stApp {
    background-color: #0e1117;
    color: white;
}
.big-title {
    font-size: 34px;
    font-weight: bold;
    text-align: center;
}
.subtitle {
    text-align: center;
    color: #9aa0a6;
}
.result-box {
    padding: 15px;
    border-radius: 10px;
    font-size: 20px;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# LOAD MODEL
# -----------------------------
model = pickle.load(open("model.pkl", "rb"))
vectorizer = pickle.load(open("vectorizer.pkl", "rb"))

# -----------------------------
# TEXT CLEANING
# -----------------------------
def clean_text(text):
    text = text.lower()
    text = re.sub(r'\d+', '', text)
    text = text.translate(str.maketrans('', '', string.punctuation))
    return text

# -----------------------------
# UI HEADER
# -----------------------------
st.markdown('<p class="big-title">📧 AI Spam Message Detector</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Type a message and check if it is SPAM or SAFE</p>', unsafe_allow_html=True)

st.write("")

# Input box
user_input = st.text_area("Enter your message:", height=150)

# Button
if st.button("🔍 Check Message"):

    if user_input.strip() == "":
        st.warning("Please enter a message first.")
    else:
        cleaned = clean_text(user_input)
        vectorized = vectorizer.transform([cleaned])
        prediction = model.predict(vectorized)[0]

        st.write("")

        if prediction == "spam":
            st.markdown(
                '<div class="result-box" style="background-color:#3a0d11;color:#ff4b4b;">🚨 SPAM MESSAGE DETECTED</div>',
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                '<div class="result-box" style="background-color:#0f2e1d;color:#00ffae;">✅ SAFE MESSAGE</div>',
                unsafe_allow_html=True
            )
