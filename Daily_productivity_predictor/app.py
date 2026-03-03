# app.py

import streamlit as st
import pandas as pd
import pickle
from docx import Document
import io
import random

# ---------------- LOAD MODEL ----------------
# ---------------- LOAD MODEL (FIXED FOR STREAMLIT CLOUD) ----------------
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
st.markdown("### Smart Lifestyle • Stress Prediction • Fitness & Diet Planning")
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
    food_type = st.selectbox("Type of Food You Eat",
                             ["Vegetarian", "Non-Vegetarian", "Vegan"])
    want_diet = st.radio("Do you want a personalized diet plan?", ["Yes", "No"])

st.markdown("---")

# ---------------- WORKOUT SECTION ----------------
st.header("🏋️ Choose Your Workout Preference")

workout_type = st.selectbox(
    "What type of workout do you prefer?",
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

    # -------- Health Analysis --------
    analysis = []

    if sleep_hours < 6:
        analysis.append("⚠️ Sleep is below optimal level. Improve sleep hygiene.")
    else:
        analysis.append("✅ Sleep duration is healthy.")

    if physical_activity < 1:
        analysis.append("⚠️ Increase physical activity for better energy and focus.")
    else:
        analysis.append("✅ Physical activity level is good.")

    if water < 2:
        analysis.append("⚠️ Increase hydration to 2–3 liters daily.")
    else:
        analysis.append("✅ Hydration level is adequate.")

    if stress_level == "High":
        analysis.append("🚨 High stress detected. Implement structured breaks & mindfulness.")
    elif stress_level == "Medium":
        analysis.append("⚡ Moderate stress. Maintain balanced routine.")
    else:
        analysis.append("🌿 Low stress. Keep maintaining healthy habits.")

    # -------- GENERAL DIET --------
    general_diet = [
        "Breakfast: Whole grains + Protein",
        "Lunch: Balanced carbs + Vegetables + Protein",
        "Snack: Fruits / Nuts",
        "Dinner: Light meal with protein + fiber",
        "Water: 2-3 liters daily"
    ]

    # -------- PERSONALIZED DIET --------
    personalized_diet = []

    if want_diet == "Yes":

        if food_type == "Vegetarian":
            protein_source = "Paneer / Lentils / Tofu"
        elif food_type == "Non-Vegetarian":
            protein_source = "Eggs / Chicken / Fish"
        else:
            protein_source = "Tofu / Beans / Plant protein"

        if bmi_status == "Underweight":
            goal = "Increase calorie intake with healthy fats."
        elif bmi_status == "Normal":
            goal = "Maintain balanced nutrition."
        elif bmi_status == "Overweight":
            goal = "Reduce processed carbs and increase protein."
        else:
            goal = "Follow calorie-controlled high-protein diet."

        personalized_diet = [
            f"Goal: {goal}",
            f"Protein Source: {protein_source}",
            "Breakfast: High-protein meal",
            "Lunch: Controlled carbs + Vegetables + Protein",
            "Snack: Healthy fats + fruits",
            "Dinner: Light protein-focused meal",
            "Hydration: 2.5 liters water"
        ]

    # -------- WORKOUT PLAN --------
    if workout_type == "Gym Training":
        workout_plan = [
            "Mon: Chest + Triceps",
            "Tue: Back + Biceps",
            "Wed: Cardio",
            "Thu: Legs",
            "Fri: Shoulders",
            "Sat: Core",
            "Sun: Rest"
        ]
    elif workout_type == "Home Workout":
        workout_plan = [
            "Mon: Push-ups + Squats",
            "Tue: Core Training",
            "Wed: Jump Rope",
            "Thu: Lunges + Abs",
            "Fri: Full Body Workout",
            "Sat: Stretching",
            "Sun: Rest"
        ]
    elif workout_type == "Yoga Only":
        workout_plan = [
            "Daily: Surya Namaskar (10 rounds)",
            "Pranayama (15 mins)",
            "Meditation (15 mins)"
        ]
    elif workout_type == "Cardio Focus":
        workout_plan = [
            "Mon: Running",
            "Tue: Cycling",
            "Wed: HIIT",
            "Thu: Brisk Walk",
            "Fri: Skipping",
            "Sat: Swimming",
            "Sun: Rest"
        ]
    else:
        workout_plan = [
            "3 Days Strength Training",
            "2 Days Cardio",
            "1 Day Yoga",
            "1 Day Complete Rest"
        ]

    # -------- DISPLAY --------
    st.header("📊 AI Wellness Summary")
    st.subheader(f"Predicted Stress Level: {stress_level}")
    st.write(f"Your BMI: {round(bmi,2)} ({bmi_status})")

    st.subheader("🔎 Health Analysis")
    for a in analysis:
        st.write("-", a)

    st.subheader("🏋️ Weekly Workout Plan")
    for w in workout_plan:
        st.write("-", w)

    # -------- Diet Display --------
    if want_diet == "Yes":
        st.markdown("## 🥗 ⭐ PERSONALIZED DIET PLAN ⭐")
        for d in personalized_diet:
            st.write("-", d)
    else:
        st.markdown("## 🥗 General Healthy Diet Plan")
        for d in general_diet:
            st.write("-", d)

    # -------- Motivation --------
    st.subheader("🔥 Motivation & Growth Guidance")
    quote = random.choice([
        "Success is built daily, not in a day.",
        "Discipline beats motivation.",
        "Your future self is watching you right now."
    ])
    st.write("💬", quote)

    # -------- Word Report --------
    doc = Document()
    doc.add_heading("AI Wellness & Performance Report", 0)
    doc.add_paragraph(f"Stress Level: {stress_level}")
    doc.add_paragraph(f"BMI: {round(bmi,2)} ({bmi_status})")

    doc.add_heading("Health Analysis", level=1)
    for a in analysis:
        doc.add_paragraph(a, style="List Bullet")

    doc.add_heading("Weekly Workout Plan", level=1)
    for w in workout_plan:
        doc.add_paragraph(w, style="List Bullet")

    if want_diet == "Yes":
        doc.add_heading("Personalized Diet Plan", level=1)
        for d in personalized_diet:
            doc.add_paragraph(d, style="List Bullet")
    else:
        doc.add_heading("General Diet Plan", level=1)
        for d in general_diet:
            doc.add_paragraph(d, style="List Bullet")

    buffer = io.BytesIO()
    doc.save(buffer)

    st.download_button(
        "⬇️ Download Full Wellness Report (DOCX)",
        data=buffer.getvalue(),
        file_name="AI_Wellness_Report.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"

    )
