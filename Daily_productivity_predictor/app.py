# app.py

import streamlit as st
import pandas as pd
import pickle
from docx import Document
import io
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
st.markdown("### Adaptive Lifestyle Intelligence System")
st.markdown("---")

# ---------------- INPUT SECTION ----------------
st.header("📋 Enter Your Details")

col1, col2 = st.columns(2)

with col1:
    name = st.text_input("Your Name")
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

    workout_type = st.selectbox(
        "Preferred Workout Type",
        ["Weight Loss", "Muscle Gain", "General Fitness", "Stress Relief"]
    )

    excel_field = st.selectbox(
        "Field You Want To Excel In",
        ["Academics", "AI/ML", "Coding", "Public Speaking", "Business", "Fitness"]
    )

st.markdown("---")

if st.button("Generate Smart AI Report"):

    st.balloons()
    st.success("🎉 Your Personalized AI Report is Ready!")

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
        (motivation * 6) -
        (career_stress * 5)
    )
    productivity_score = max(0, min(productivity_score, 100))

    mental_balance = int(
        (sleep_hours * 12) +
        (water * 8) -
        (career_stress * 6)
    )
    mental_balance = max(0, min(mental_balance, 100))

    burnout_risk = career_stress * 10 - sleep_hours * 5

    # -------- Diet Plan --------
    if bmi_status == "Underweight":
        diet_plan = [
            "Increase healthy carbs",
            "Add nuts & peanut butter",
            "Protein shake daily"
        ]
    elif bmi_status == "Overweight":
        diet_plan = [
            "High protein, low refined carbs",
            "Avoid sugary drinks",
            "Eat salad before meals"
        ]
    else:
        diet_plan = [
            "Balanced diet",
            "2 fruits daily",
            "Stay hydrated"
        ]

    # -------- Workout Plan --------
    if workout_type == "Weight Loss":
        workout_plan = [
            "30 min brisk walking",
            "15 min HIIT",
            "Core workout 3x/week"
        ]
    elif workout_type == "Muscle Gain":
        workout_plan = [
            "Push-Pull-Legs split",
            "Progressive overload",
            "Protein 1.5g/kg"
        ]
    elif workout_type == "Stress Relief":
        workout_plan = [
            "Yoga 20 mins daily",
            "Deep breathing",
            "Light stretching"
        ]
    else:
        workout_plan = [
            "Full body workout 3x/week",
            "Cardio 2x/week"
        ]

    # -------- Excellence Plan --------
    if excel_field == "AI/ML":
        excel_plan = [
            "Study ML theory 2 hrs daily",
            "Build 1 mini project weekly",
            "Practice Kaggle problems"
        ]
    elif excel_field == "Coding":
        excel_plan = [
            "Solve 2 DSA problems daily",
            "Build real projects",
            "Contribute to GitHub"
        ]
    elif excel_field == "Business":
        excel_plan = [
            "Learn marketing basics",
            "Read 1 business case weekly",
            "Work on side hustle"
        ]
    else:
        excel_plan = [
            "Daily focused practice",
            "Track weekly progress",
            "Seek mentorship"
        ]

    # -------- Tabs --------
    tab1, tab2, tab3 = st.tabs([
        "📊 Overview",
        "🥗 Health & Fitness",
        "🚀 Growth Strategy"
    ])

    # -------- TAB 1 --------
    with tab1:
        st.subheader(f"Performance Overview - {name}")
        st.success(f"Predicted Stress Level: {stress_level}")
        st.write(f"BMI: {round(bmi,2)} ({bmi_status})")

        st.metric("Productivity Score", f"{productivity_score}/100")
        st.metric("Mental Balance", f"{mental_balance}/100")

        if burnout_risk > 50:
            st.error("⚠ High Burnout Risk Detected")

        if water < 1.5:
            st.warning("Increase water intake to at least 2L daily.")

        # Bar Chart
        scores = {
            "Productivity": productivity_score,
            "Mental Balance": mental_balance,
            "Fitness": physical_activity * 25,
            "Hydration": water * 20
        }

        fig, ax = plt.subplots()
        ax.bar(scores.keys(), scores.values())
        ax.set_ylim(0, 100)
        ax.set_ylabel("Score")
        st.pyplot(fig)

        # Pie Chart
        time_data = {
            "Study": study_hours,
            "Sleep": sleep_hours,
            "Social": social_hours,
            "Physical": physical_activity
        }

        fig2, ax2 = plt.subplots()
        ax2.pie(time_data.values(), labels=time_data.keys(), autopct='%1.1f%%')
        ax2.set_title("Daily Time Distribution")
        st.pyplot(fig2)

    # -------- TAB 2 --------
    with tab2:
        st.subheader("🥗 Smart Diet Plan")
        for d in diet_plan:
            st.write("•", d)

        st.subheader("🏋 Personalized Workout Plan")
        for w in workout_plan:
            st.write("•", w)

    # -------- TAB 3 --------
    with tab3:
        st.subheader("🚀 Excellence Blueprint")
        for e in excel_plan:
            st.write("•", e)

    # -------- DOCX REPORT --------
    doc = Document()
    doc.add_heading("AI Adaptive Wellness Report", 0)
    doc.add_paragraph(f"Name: {name}")
    doc.add_paragraph(f"Stress Level: {stress_level}")
    doc.add_paragraph(f"Productivity Score: {productivity_score}")
    doc.add_paragraph(f"Mental Balance: {mental_balance}")
    doc.add_paragraph("Diet Plan:")
    for d in diet_plan:
        doc.add_paragraph(d, style="List Bullet")

    buffer = io.BytesIO()
    doc.save(buffer)

    st.download_button(
        "⬇ Download Full AI Report",
        data=buffer.getvalue(),
        file_name="AI_Wellness_Report.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )


