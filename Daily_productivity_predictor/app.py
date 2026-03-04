# app.py

import streamlit as st
import pandas as pd
import numpy as np
from docx import Document
import io
import plotly.graph_objects as go

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AI Wellness & Performance Analyzer",
    page_icon="🧠",
    layout="wide"
)

# ---------------- CINEMATIC BACKGROUND ----------------
st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(rgba(0,0,0,0.35), rgba(0,0,0,0.35)),
                    url('https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=1950&q=80') no-repeat center center fixed;
        background-size: cover;
        color: white;
        font-family: 'Segoe UI', sans-serif;
    }
    h1, h2, h3 {
        color: #00F5FF;
        font-weight: 700;
        text-shadow: 2px 2px 8px #000000;
    }
    .glass {
        background: rgba(0,0,0,0.6);
        padding: 25px;
        border-radius: 20px;
        backdrop-filter: blur(18px);
        margin-bottom: 20px;
        box-shadow: 0 0 20px #000000;
    }
    .metric-box {
        background: rgba(0,0,0,0.6);
        border-radius: 15px;
        padding: 15px;
        text-align: center;
        box-shadow: 0 0 12px #111111;
    }
    .panda {
        position: fixed;
        bottom: 10px;
        right: 10px;
        width: 120px;
        z-index: 9999;
        animation: float 3s infinite;
    }
    @keyframes float {
        0% { transform: translateY(0); }
        50% { transform: translateY(-10px); }
        100% { transform: translateY(0); }
    }
    .chat-bubble {
        background-color: rgba(0, 245, 255, 0.2);
        padding: 10px 15px;
        border-radius: 12px;
        margin-bottom: 10px;
        box-shadow: 0 0 10px #111111;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ---------------- APP TITLE ----------------
st.markdown('<div class="glass"><h1>🧠 AI Wellness & Performance Analyzer</h1></div>', unsafe_allow_html=True)
st.markdown('<div class="glass"><h3>Smart Lifestyle • Stress Prediction • Fitness • Career Blueprint • Human-Robo Guide</h3></div>', unsafe_allow_html=True)

# ---------------- USER INPUT ----------------
st.header("📋 Enter Your Details")
name = st.text_input("Your Name")

col1, col2 = st.columns(2)
with col1:
    study_hours = st.number_input("Study Hours (per day)", 0, 12, 4)
    sleep_hours = st.number_input("Sleep Hours", 0, 12, 7)
    physical_activity = st.number_input("Workout Hours", 0, 4, 1)
    social_hours = st.number_input("Social Hours", 0, 6, 2)
    gpa = st.number_input("GPA", 0.0, 10.0, 8.0, 0.1)
    weight = st.number_input("Weight (kg)", 30, 200, 65)
    height = st.number_input("Height (cm)", 100, 220, 165)

with col2:
    career_stress = st.slider("Career Stress (1-10)", 1, 10, 5)
    motivation = st.slider("Motivation Level (1-10)", 1, 10, 7)
    water = st.number_input("Water Intake (liters)", 0.0, 5.0, 2.0, 0.1)
    food_type = st.selectbox("Diet Preference", ["Vegetarian", "Non-Vegetarian", "Vegan"])
    workout_type = st.selectbox("Workout Preference",
        ["Gym Training", "Home Workout", "Yoga Only", "Cardio Focus", "Mixed Routine"])
    plan_type = st.radio("Choose Plan Type", ["Personalized Plan", "Generalized Plan"])

st.header("🎯 Career Direction")
career_domain = st.selectbox(
    "Select Career Domain",
    ["Management", "IT & Data", "Government Exams", "Creative Field", "Entrepreneurship"]
)
career_niche = st.text_input("Specific Niche (Example: Data Science, MBA Finance, UPSC, UI/UX)")

st.markdown("---")

# ---------------- AI PREDICTION FUNCTION ----------------
def ai_prediction(study, sleep, workout, social, motivation, career_stress, bmi, water):
    stress_score = max(1, min(10, int(career_stress + (8 - sleep) + (5 - workout) * 1.5)))
    if stress_score >= 8:
        stress_text = "High Stress! Prioritize sleep, mindfulness, and breaks."
    elif stress_score >= 5:
        stress_text = "Moderate Stress. Maintain schedule and recovery cycles."
    else:
        stress_text = "Low Stress. Keep up healthy habits!"

    productivity_score = max(0, min(100, int((sleep*10) + (workout*10) + (motivation*5) - (career_stress*4))))
    health_score = max(0, min(100, int((100 - abs(22-bmi)*5) + workout*5 + water*5)))

    tips = []
    if sleep < 6:
        tips.append("Increase sleep to at least 7 hours for better recovery.")
    if workout < 1:
        tips.append("Include at least 30 min of physical activity daily.")
    if water < 2:
        tips.append("Drink at least 2 liters of water per day.")
    if motivation < 5:
        tips.append("Set small achievable goals to boost motivation.")
    if career_stress > 7:
        tips.append("Practice mindfulness or meditation to reduce career stress.")

    return stress_score, stress_text, productivity_score, health_score, tips

# ---------------- HUMAN ROBO GUIDE ----------------
st.sidebar.header("🤖 Human-Robo Guide")
user_message = st.sidebar.text_area("Ask me for advice or tips:", "")
if st.sidebar.button("Send") and user_message.strip() != "":
    # Simple AI responses based on keywords
    response = "Hello! I am your Human-Robo Guide 🤖. Here's some advice:\n"
    if "sleep" in user_message.lower():
        response += "- Ensure 7-8 hours of quality sleep daily.\n"
    if "stress" in user_message.lower():
        if career_stress > 7:
            response += "- You have high stress, try meditation and short breaks.\n"
        else:
            response += "- Your stress is moderate, keep consistent routines.\n"
    if "workout" in user_message.lower() or "exercise" in user_message.lower():
        response += "- Physical activity improves mood and productivity.\n"
    if "diet" in user_message.lower() or "food" in user_message.lower():
        response += "- Stay hydrated and balance protein, carbs, and veggies.\n"
    if "motivation" in user_message.lower():
        response += "- Set achievable goals and reward yourself for progress.\n"
    if response == "Hello! I am your Human-Robo Guide 🤖. Here's some advice:\n":
        response += "- Keep maintaining a balanced lifestyle and stay consistent!\n"
    
    st.sidebar.markdown(f'<div class="chat-bubble">{response}</div>', unsafe_allow_html=True)

# ---------------- GENERATE REPORT ----------------
if st.button("Generate Full AI Wellness Report"):

    st.balloons()
    
    bmi = weight / ((height / 100) ** 2)
    stress_score, stress_text, productivity_score, health_score, tips = ai_prediction(
        study_hours, sleep_hours, physical_activity, social_hours, motivation, career_stress, bmi, water
    )

    st.markdown(f'<div class="glass"><h2>💬 Dear {name}, Here Is Your AI Wellness Prediction & Tips</h2></div>', unsafe_allow_html=True)
    colA, colB, colC = st.columns(3)
    colA.metric("Stress Level", f"{stress_score}/10")
    colB.metric("Productivity Score", f"{productivity_score}/100")
    colC.metric("Health Score", f"{health_score}/100")
    
    st.subheader("📝 Personalized Tips for You")
    for tip in tips:
        st.write(f"- {tip}")

# ---------------- REPORT DOWNLOAD ----------------
if st.button("Download Consultant Report"):

    st.balloons()
    
    doc = Document()
    doc.add_heading("🧠 AI Wellness Consultant Report", 0)
    doc.add_paragraph(f"Dear {name}, here is your personalized consultation report:\n")
    doc.add_paragraph(f"Stress Level: {stress_score}/10\nAdvice: {stress_text}\n")
    doc.add_paragraph(f"Productivity Score: {productivity_score}/100\nHealth Score: {health_score}/100\n")
    doc.add_paragraph("Personalized Tips:")
    for tip in tips:
        doc.add_paragraph(f"- {tip}")

    buffer = io.BytesIO()
    doc.save(buffer)
    st.download_button(
        "⬇️ Download Consultant Report",
        data=buffer.getvalue(),
        file_name="AI_Wellness_Consultant_Report.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )
