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
st.markdown("### Smart Lifestyle • Stress Prediction • Fitness • Career Blueprint")
st.markdown("---")

# ---------------- INPUT SECTION ----------------
st.header("📋 Enter Your Details")

name = st.text_input("Your Name")

col1, col2 = st.columns(2)

with col1:
    study_hours = st.number_input("Study Hours (per day)", 0, 12, 4)
    sleep_hours = st.number_input("Sleep Hours", 0, 12, 7)
    physical_activity = st.number_input("Physical Activity (hours)", 0, 4, 1)
    social_hours = st.number_input("Social Hours", 0, 6, 2)
    gpa = st.number_input("GPA", 0.0, 10.0, 8.0, 0.1)
    weight = st.number_input("Weight (kg)", 30, 200, 65)
    height = st.number_input("Height (cm)", 100, 220, 165)

with col2:
    career_stress = st.slider("Career/Study Stress (1-10)", 1, 10, 5)
    motivation = st.slider("Motivation Level (1-10)", 1, 10, 7)
    water = st.number_input("Water Intake (liters)", 0.0, 5.0, 2.0, 0.1)
    food_type = st.selectbox("Diet Preference", ["Vegetarian", "Non-Vegetarian", "Vegan"])
    workout_type = st.selectbox("Workout Preference",
        ["Gym Training", "Home Workout", "Yoga Only", "Cardio Focus", "Mixed Routine"]
    )
    career_goal = st.text_input("Field You Want to Excel In (e.g., Data Science, UPSC, MBA, etc.)")

st.markdown("---")

# ---------------- GENERATE REPORT ----------------
if st.button("Generate Full AI Wellness Report"):

    st.balloons()

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
    bmi_status = "Normal"
    if bmi < 18.5:
        bmi_status = "Underweight"
    elif bmi > 24.9:
        bmi_status = "Overweight"

    # -------- Scores --------
    productivity_score = int((sleep_hours * 10) +
                             (physical_activity * 15) +
                             (motivation * 5) -
                             (career_stress * 4))
    productivity_score = max(0, min(productivity_score, 100))

    health_score = int((100 - abs(22 - bmi) * 5) +
                       (physical_activity * 10) +
                       (water * 5))
    health_score = max(0, min(health_score, 100))

    # -------- Consultant Tone --------
    st.markdown(f"## 💬 Dear {name}, Here Is Your Personalized AI Analysis")

    # ---------------- LIFESTYLE BAR CHART ----------------
    st.subheader("📊 Lifestyle Analytics")

    categories = ["Sleep", "Study", "Workout", "Water", "Motivation"]
    values = [sleep_hours, study_hours, physical_activity, water, motivation]

    fig, ax = plt.subplots()
    ax.bar(categories, values)
    ax.set_ylabel("Hours / Level")
    st.pyplot(fig)

    # ---------------- DIET SYSTEM ----------------
    st.subheader("🥗 Personalized Diet Strategy")

    if food_type == "Vegetarian":
        diet_plan = [
            "Breakfast: Oats + Milk + Nuts",
            "Lunch: Dal + Brown Rice + Paneer + Salad",
            "Snack: Roasted chana / fruits",
            "Dinner: Multigrain roti + Veg sabzi + Curd"
        ]
    elif food_type == "Vegan":
        diet_plan = [
            "Breakfast: Smoothie (Banana + Peanut Butter + Almond milk)",
            "Lunch: Quinoa + Chickpeas + Vegetables",
            "Snack: Nuts + Seeds mix",
            "Dinner: Tofu stir fry + Salad"
        ]
    else:
        diet_plan = [
            "Breakfast: Eggs + Whole wheat toast",
            "Lunch: Grilled chicken + Rice + Veggies",
            "Snack: Greek yogurt",
            "Dinner: Fish/Chicken soup + Salad"
        ]

    for item in diet_plan:
        st.write("-", item)

    # ---------------- WORKOUT PLAN ----------------
    st.subheader("🏋 Structured Weekly Workout Plan")

    if workout_type == "Gym Training":
        workout_plan = [
            "Monday: Chest + Triceps",
            "Tuesday: Back + Biceps",
            "Wednesday: Legs",
            "Thursday: Shoulders",
            "Friday: Core + Cardio"
        ]
    elif workout_type == "Home Workout":
        workout_plan = [
            "Pushups + Squats",
            "Lunges + Planks",
            "Jump rope (15 mins)",
            "Core strengthening"
        ]
    elif workout_type == "Yoga Only":
        workout_plan = [
            "Surya Namaskar (10 rounds)",
            "Pranayama (10 mins)",
            "Meditation (15 mins)"
        ]
    elif workout_type == "Cardio Focus":
        workout_plan = [
            "Running 30 mins",
            "Cycling 20 mins",
            "HIIT (15 mins)"
        ]
    else:
        workout_plan = [
            "Strength (3 days)",
            "Cardio (2 days)",
            "Yoga (1 day)"
        ]

    for w in workout_plan:
        st.write("-", w)

    # ---------------- 90 DAY CAREER BLUEPRINT ----------------
    st.subheader("🚀 90-Day Career Blueprint")

    st.write(f"Dear {name}, since you want to excel in **{career_goal}**, here is your 3-phase roadmap:")

    st.write("### Phase 1 (Days 1-30): Foundation")
    st.write("- Learn core fundamentals")
    st.write("- Study 2-3 hours daily")
    st.write("- Build basic project")

    st.write("### Phase 2 (Days 31-60): Skill Building")
    st.write("- Intermediate topics")
    st.write("- 1 Major Project")
    st.write("- Start networking on LinkedIn")

    st.write("### Phase 3 (Days 61-90): Execution")
    st.write("- Advanced project")
    st.write("- Mock interviews / practice tests")
    st.write("- Apply to internships/jobs")

    # ---------------- WEEKLY STRATEGY CHART ----------------
    st.subheader("⏳ Weekly Time Strategy")

    week_data = {
        "Study": study_hours * 7,
        "Workout": physical_activity * 7,
        "Sleep": sleep_hours * 7
    }

    fig2, ax2 = plt.subplots()
    ax2.bar(week_data.keys(), week_data.values())
    ax2.set_ylabel("Hours per Week")
    st.pyplot(fig2)

    # ---------------- MOTIVATION QUOTE ----------------
    quotes = [
        "Discipline beats motivation.",
        "Your future is built daily.",
        "Small consistency creates big success."
    ]

    st.subheader("💬 Final Consultant Advice")
    st.success(random.choice(quotes))

    # ---------------- DOCX REPORT ----------------
    doc = Document()
    doc.add_heading("AI Wellness & Performance Report", 0)
    doc.add_paragraph(f"Name: {name}")
    doc.add_paragraph(f"Stress Level: {stress_level}")
    doc.add_paragraph(f"BMI: {round(bmi,2)} ({bmi_status})")
    doc.add_paragraph(f"Productivity Score: {productivity_score}/100")
    doc.add_paragraph(f"Health Score: {health_score}/100")
    doc.add_paragraph(f"Career Goal: {career_goal}")

    doc.add_heading("Diet Plan", level=1)
    for item in diet_plan:
        doc.add_paragraph(item)

    doc.add_heading("Workout Plan", level=1)
    for w in workout_plan:
        doc.add_paragraph(w)

    buffer = io.BytesIO()
    doc.save(buffer)

    st.download_button(
        "⬇️ Download Full Professional Report",
        data=buffer.getvalue(),
        file_name="AI_Wellness_Report.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )


