# app.py

import streamlit as st
import pandas as pd
import pickle
from docx import Document
import io
import random
import matplotlib.pyplot as plt
import numpy as np

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AI Wellness & Performance Analyzer",
    page_icon="🧠",
    layout="wide"
)

# ---------------- DARK UI ----------------
st.markdown("""
    <style>
        .stApp {
            background-color: #0E1117;
            color: white;
        }
        h1, h2, h3 {
            color: #00F5FF;
        }
    </style>
""", unsafe_allow_html=True)

st.title("🧠 AI Wellness & Performance Analyzer")
st.markdown("### Smart Lifestyle • Stress Prediction • Fitness • Career Blueprint")
st.markdown("---")

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(BASE_DIR, "models", "productivity_model.pkl")
LE_PATH = os.path.join(BASE_DIR, "models", "label_encoder.pkl")

with open(MODEL_PATH, "rb") as f:
    model = pickle.load(f)

with open(LE_PATH, "rb") as f:
    le = pickle.load(f)

# ---------------- INPUT SECTION ----------------
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

st.markdown("---")

# ---------------- CAREER SECTION ----------------
st.header("🎯 Career Direction")

career_domain = st.selectbox(
    "Select Your Career Domain",
    ["Management", "IT & Data", "Government Exams", "Creative Field", "Entrepreneurship"]
)

career_niche = st.text_input("Select Your Specific Niche")

st.markdown("---")

# ---------------- GENERATE REPORT ----------------
if st.button("Generate Full AI Wellness Report"):

    st.balloons()

    # Prediction
    input_df = pd.DataFrame({
        "Study_Hours_Per_Day": [study_hours],
        "Extracurricular_Hours_Per_Day": [1],
        "Sleep_Hours_Per_Day": [sleep_hours],
        "Social_Hours_Per_Day": [social_hours],
        "Physical_Activity_Hours_Per_Day": [physical_activity],
        "GPA": [gpa]
    })

    prediction = model.predict(input_df)
    stress_level = le.inverse_transform(prediction)[0]

    # Model confidence
    confidence = None
    if hasattr(model, "predict_proba"):
        proba = model.predict_proba(input_df)
        confidence = round(max(proba[0]) * 100, 2)

    # BMI
    bmi = weight / ((height / 100) ** 2)

    # Scores
    productivity_score = int((sleep_hours * 10) +
                             (physical_activity * 15) +
                             (motivation * 5) -
                             (career_stress * 4))
    productivity_score = max(0, min(productivity_score, 100))

    health_score = int((100 - abs(22 - bmi) * 5) +
                       (physical_activity * 10) +
                       (water * 5))
    health_score = max(0, min(health_score, 100))

    # ---------------- KPI METRICS ----------------
    st.markdown(f"## 💬 Dear {name}, Here Is Your AI Dashboard")

    colA, colB, colC = st.columns(3)
    colA.metric("🧠 Stress Level", stress_level)
    colB.metric("⚡ Productivity", f"{productivity_score}/100")
    colC.metric("💪 Health Score", f"{health_score}/100")

    if confidence:
        st.write(f"Model Confidence: {confidence}%")

    st.progress(productivity_score / 100)

    # ---------------- BAR CHART ----------------
    st.subheader("⏳ Weekly Time Distribution")

    weekly_data = {
        "Study": study_hours * 7,
        "Workout": physical_activity * 7,
        "Sleep": sleep_hours * 7
    }

    fig, ax = plt.subplots(figsize=(5,3), facecolor="#0E1117")
    ax.set_facecolor("#0E1117")
    ax.bar(weekly_data.keys(), weekly_data.values(),
           color=["#00F5FF", "#FF2E63", "#08F7FE"])
    ax.tick_params(colors="white")
    ax.set_ylabel("Hours", color="white")
    st.pyplot(fig)

    # ---------------- HEATMAP ----------------
    st.subheader("🔥 Lifestyle Balance Heatmap")

    heat_data = np.array([
        [sleep_hours/12, study_hours/12],
        [physical_activity/4, motivation/10]
    ])

    fig2, ax2 = plt.subplots(figsize=(4,3), facecolor="#0E1117")
    ax2.set_facecolor("#0E1117")
    im = ax2.imshow(heat_data, cmap="cool")
    ax2.set_xticks([0,1])
    ax2.set_yticks([0,1])
    ax2.set_xticklabels(["Health", "Growth"], color="white")
    ax2.set_yticklabels(["Physical", "Mental"], color="white")
    plt.colorbar(im)
    st.pyplot(fig2)

    # ---------------- RISK DETECTION ----------------
    st.subheader("⚠ Risk Detection")

    if sleep_hours < 6:
        st.warning("Low sleep detected.")
    if water < 1.5:
        st.warning("Low hydration detected.")
    if career_stress > 8:
        st.error("High stress alert.")

    # ---------------- AI RECOMMENDATIONS ----------------
    st.subheader("🤖 Smart AI Recommendations")

    if productivity_score < 40:
        st.write("- Fix sleep schedule.")
        st.write("- Reduce distractions.")
    elif productivity_score < 75:
        st.write("- Increase deep work blocks.")
    else:
        st.write("- Maintain discipline and scale performance.")

    # ---------------- DIET PLAN ----------------
    st.subheader("🥗 Personalized Diet Plan")

    if food_type == "Vegetarian":
        diet_plan = ["Oats + Milk", "Dal + Rice", "Fruits", "Roti + Sabzi"]
    elif food_type == "Vegan":
        diet_plan = ["Smoothie", "Quinoa + Veggies", "Nuts", "Tofu"]
    else:
        diet_plan = ["Eggs", "Chicken + Rice", "Yogurt", "Fish"]

    for d in diet_plan:
        st.write("-", d)

    # ---------------- WORKOUT PLAN ----------------
    st.subheader("🏋 Structured Workout Plan")

    workout_plan = {
        "Gym Training": ["Chest", "Back", "Legs", "Shoulders"],
        "Home Workout": ["Pushups", "Squats", "Planks"],
        "Yoga Only": ["Surya Namaskar", "Pranayama"],
        "Cardio Focus": ["Running", "Cycling"],
        "Mixed Routine": ["Strength", "Cardio", "Yoga"]
    }

    for w in workout_plan[workout_type]:
        st.write("-", w)

    # ---------------- 90 DAY CAREER PLAN ----------------
    st.subheader("🚀 90-Day Career Blueprint")

    st.write(f"Domain: {career_domain}")
    st.write(f"Niche: {career_niche}")

    st.write("Days 1–30: Build Foundation")
    st.write("Days 31–60: Advanced Skill + Project")
    st.write("Days 61–90: Mock + Apply + Execute")

    # ---------------- FINAL MOTIVATION ----------------
    st.subheader("💬 Final Consultant Advice")

    st.markdown(f"""
Dear {name},

Consistency in **{career_niche}** for 90 days can redefine your trajectory.

Discipline > Motivation  
Action > Overthinking  
Execution > Excuses
""")

    # ---------------- DOCX REPORT ----------------
    doc = Document()
    doc.add_heading("AI Wellness Report", 0)
    doc.add_paragraph(f"Name: {name}")
    doc.add_paragraph(f"Stress Level: {stress_level}")
    doc.add_paragraph(f"Productivity: {productivity_score}")
    doc.add_paragraph(f"Health Score: {health_score}")
    doc.add_paragraph(f"Career Domain: {career_domain}")
    doc.add_paragraph(f"Career Niche: {career_niche}")

    buffer = io.BytesIO()
    doc.save(buffer)

    st.download_button(
        "⬇️ Download Full Professional Report",
        data=buffer.getvalue(),
        file_name="AI_Wellness_Report.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )




