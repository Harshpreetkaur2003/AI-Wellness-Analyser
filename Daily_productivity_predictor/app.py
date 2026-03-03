# app.py

import streamlit as st
import pandas as pd
import pickle
from docx import Document
import io
import random
import matplotlib.pyplot as plt
import numpy as np

# ---------------- LOAD MODEL ----------------
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(BASE_DIR, "models", "productivity_model.pkl")
LE_PATH = os.path.join(BASE_DIR, "models", "label_encoder.pkl")

with open(MODEL_PATH, "rb") as f:
    model = pickle.load(f)

with open(LE_PATH, "rb") as f:
    le = pickle.load(f)
# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AI Wellness & Performance Analyzer",
    page_icon="🧠",
    layout="wide"
)

st.title("🧠 AI Wellness & Performance Analyzer")
st.markdown("### Smart Lifestyle • Stress Prediction • Fitness • Mental Growth")
st.markdown("---")

# ---------------- INPUT SECTION ----------------
st.header("📋 Enter Your Details")

col1, col2 = st.columns(2)

with col1:
    study_hours = st.number_input("Study Hours (per day)", 0, 12, 4)
    sleep_hours = st.number_input("Sleep Hours", 0, 12, 7)
    physical_activity = st.number_input("Physical Activity (hours)", 0, 4, 1)
    social_hours = st.number_input("Social Hours", 0, 6, 2)
    gpa = st.number_input("GPA", 0.0, 10.0, 8.0, 0.1)
    gender = st.radio("Gender", ["Male", "Female", "Other"])
    weight = st.number_input("Weight (kg)", 30, 200, 65)
    height = st.number_input("Height (cm)", 100, 220, 165)

with col2:
    career_stress = st.slider("Career/Study Stress (1-10)", 1, 10, 5)
    motivation = st.slider("Motivation Level (1-10)", 1, 10, 7)
    water = st.number_input("Water Intake (liters)", 0.0, 5.0, 2.0, 0.1)
    food_type = st.selectbox(
        "Type of Food You Eat",
        ["Vegetarian", "Non-Vegetarian", "Vegan"]
    )
    want_diet = st.radio("Do you want a personalized diet plan?", ["Yes", "No"])

st.markdown("---")

# ---------------- WORKOUT SECTION ----------------
st.header("🏋️ Choose Your Workout Preference")

workout_type = st.selectbox(
    "Workout Preference",
    ["Gym Training", "Home Workout", "Yoga Only", "Cardio Focus", "Mixed Routine"]
)

st.markdown("---")

# ---------------- GENERATE REPORT ----------------
if st.button("Generate Full AI Wellness Report"):

    # -------- Prediction --------
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

    # -------- BMI --------
    bmi = weight / ((height / 100) ** 2)

    if bmi < 18.5:
        bmi_status = "Underweight"
    elif bmi < 24.9:
        bmi_status = "Normal"
    elif bmi < 29.9:
        bmi_status = "Overweight"
    else:
        bmi_status = "Obese"

    # -------- Scores --------
    productivity_score = int(
        (sleep_hours * 10) +
        (physical_activity * 15) +
        (motivation * 5) -
        (career_stress * 4)
    )
    productivity_score = max(0, min(productivity_score, 100))

    health_score = int(
        (100 - abs(22 - bmi) * 5) +
        (physical_activity * 10) +
        (water * 5)
    )
    health_score = max(0, min(health_score, 100))

    # -------- Burnout Risk --------
    burnout_risk = "Low"
    if career_stress > 7 and sleep_hours < 6:
        burnout_risk = "High"
    elif career_stress > 5:
        burnout_risk = "Moderate"

    # -------- Workout Plan --------
    workout_plan = [
        "Strength Training (3 days)",
        "Cardio (2 days)",
        "Stretching/Yoga (1 day)",
        "1 Full Rest Day"
    ]

    # -------- Diet --------
    general_diet = [
        "Breakfast: Whole grains + Protein",
        "Lunch: Balanced carbs + Vegetables + Protein",
        "Snack: Fruits / Nuts",
        "Dinner: Light meal with protein + fiber",
        "Water: 2-3 liters daily"
    ]

    # ---------------- DASHBOARD ----------------
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Dashboard",
        "🏋️ Fitness",
        "🧠 Mental Health",
        "🎯 Goals & Growth"
    ])

    # -------- TAB 1 --------
    with tab1:
        st.subheader("Stress & Health Overview")
        st.success(f"Predicted Stress Level: {stress_level}")
        st.write(f"BMI: {round(bmi,2)} ({bmi_status})")

        st.metric("Productivity Score", f"{productivity_score}/100")
        st.progress(productivity_score / 100)

        st.metric("Health Score", f"{health_score}/100")
        st.progress(health_score / 100)

        if burnout_risk == "High":
            st.error("🚨 High Burnout Risk – Prioritize Rest & Recovery")
        elif burnout_risk == "Moderate":
            st.warning("⚠️ Moderate Burnout Risk – Improve Balance")
        else:
            st.success("✅ Low Burnout Risk – You're Managing Well")

    # -------- TAB 2 --------
    with tab2:
        st.subheader("Workout Plan")
        for w in workout_plan:
            st.write("-", w)

        st.subheader("Nutrition Guide")
        for d in general_diet:
            st.write("-", d)

    # -------- TAB 3 --------
    with tab3:
        st.subheader("Mental Health Guidance")

        if stress_level == "High":
            st.write("• Practice 10 minutes of meditation daily")
            st.write("• Follow Pomodoro (25-5 method)")
            st.write("• Limit social media usage")
        elif stress_level == "Medium":
            st.write("• Maintain work-life balance")
            st.write("• Exercise regularly")
            st.write("• Journal your thoughts weekly")
        else:
            st.write("• Continue your healthy routine")
            st.write("• Practice gratitude daily")
            st.write("• Keep challenging yourself positively")

        st.subheader("📚 Recommended Books")

        st.write("- Atomic Habits by James Clear")
        st.write("- Deep Work by Cal Newport")
        st.write("- The 7 Habits of Highly Effective People by Stephen Covey")
        st.write("- The Power of Now by Eckhart Tolle")

        st.subheader("💬 Motivational Quote")

        quotes = [
            "Small daily improvements lead to stunning long-term results.",
            "Discipline creates freedom.",
            "Your future is created by what you do today.",
            "Focus on progress, not perfection."
        ]

        st.info(random.choice(quotes))

    # -------- TAB 4 --------
    with tab4:
        st.subheader("🎯 Goal Focus Strategy")

        st.write("1️⃣ Define 1 main goal for next 30 days.")
        st.write("2️⃣ Break it into weekly milestones.")
        st.write("3️⃣ Schedule daily deep work blocks.")
        st.write("4️⃣ Track progress every Sunday.")
        st.write("5️⃣ Remove distractions during focus time.")

        st.subheader("Growth Advice")

        if productivity_score > 70:
            st.success("You are performing at a strong level. Focus on consistency.")
        elif productivity_score > 40:
            st.warning("You have potential. Improve sleep and discipline.")
        else:
            st.error("Start small. Build routines before chasing big goals.")

    # ---------------- DOCX REPORT ----------------
    doc = Document()
    doc.add_heading("AI Wellness & Performance Report", 0)
    doc.add_paragraph(f"Stress Level: {stress_level}")
    doc.add_paragraph(f"BMI: {round(bmi,2)} ({bmi_status})")
    doc.add_paragraph(f"Productivity Score: {productivity_score}/100")
    doc.add_paragraph(f"Health Score: {health_score}/100")
    doc.add_paragraph(f"Burnout Risk: {burnout_risk}")

    buffer = io.BytesIO()
    doc.save(buffer)

    st.download_button(
        "⬇️ Download Full Wellness Report (DOCX)",
        data=buffer.getvalue(),
        file_name="AI_Wellness_Report.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )


