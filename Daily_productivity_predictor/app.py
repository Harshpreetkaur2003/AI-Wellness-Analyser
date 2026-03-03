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
st.markdown("### Adaptive Lifestyle Intelligence System")
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
    weight = st.number_input("Weight (kg)", 30, 200, 65)
    height = st.number_input("Height (cm)", 100, 220, 165)

with col2:
    career_stress = st.slider("Career/Study Stress (1-10)", 1, 10, 5)
    motivation = st.slider("Motivation Level (1-10)", 1, 10, 7)
    water = st.number_input("Water Intake (liters)", 0.0, 5.0, 2.0, 0.1)

st.markdown("---")

if st.button("Generate Smart AI Report"):

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

    # -------- Intelligent Scores --------
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

    # -------- Dynamic Book Recommendation --------
    if stress_level == "High":
        book_suggestions = [
            "The Power of Now – Eckhart Tolle",
            "Why Zebras Don't Get Ulcers – Robert Sapolsky",
            "The Untethered Soul – Michael Singer"
        ]
    elif motivation < 5:
        book_suggestions = [
            "Atomic Habits – James Clear",
            "Can't Hurt Me – David Goggins",
            "The 5 AM Club – Robin Sharma"
        ]
    elif productivity_score > 75:
        book_suggestions = [
            "Deep Work – Cal Newport",
            "Essentialism – Greg McKeown",
            "The ONE Thing – Gary Keller"
        ]
    else:
        book_suggestions = [
            "Mindset – Carol Dweck",
            "Grit – Angela Duckworth",
            "The 7 Habits of Highly Effective People – Stephen Covey"
        ]

    # -------- Adaptive Quotes --------
    if stress_level == "High":
        quote = "Slow down. You don’t have to win every day to win in life."
    elif motivation < 5:
        quote = "Action creates motivation, not the other way around."
    elif productivity_score > 75:
        quote = "Mastery demands focus and consistency."
    else:
        quote = "Progress, not perfection."

    # -------- Dashboard Tabs --------
    tab1, tab2, tab3 = st.tabs([
        "📊 Overview",
        "🧠 Mental Intelligence",
        "🎯 Growth Strategy"
    ])

    # -------- TAB 1 --------
    with tab1:
        st.subheader("Performance Overview")
        st.success(f"Predicted Stress Level: {stress_level}")
        st.write(f"BMI: {round(bmi,2)} ({bmi_status})")

        st.metric("Productivity Score", f"{productivity_score}/100")
        st.progress(productivity_score / 100)

        st.metric("Mental Balance Score", f"{mental_balance}/100")
        st.progress(mental_balance / 100)

        # -------- Radar Chart --------
        categories = ["Sleep", "Activity", "Stress", "Motivation"]
        values = [
            sleep_hours * 10,
            physical_activity * 20,
            100 - (career_stress * 10),
            motivation * 10
        ]

        values += values[:1]
        angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=False).tolist()
        angles += angles[:1]

        fig, ax = plt.subplots(figsize=(5,5), subplot_kw=dict(polar=True))
        ax.plot(angles, values)
        ax.fill(angles, values, alpha=0.25)
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(categories)
        ax.set_yticklabels([])
        st.pyplot(fig)

        # -------- Colorful Bar Graph --------
        st.markdown("### 📊 Performance Statistics (Visual Overview)")

        labels = ["Productivity", "Mental Balance", "Stress Index"]
        stress_numeric = 30 if stress_level == "Low" else 60 if stress_level == "Medium" else 90
        values = [productivity_score, mental_balance, stress_numeric]
        colors = ["#00C49F", "#0088FE", "#FF4B4B"]

        fig2, ax2 = plt.subplots()
        bars = ax2.bar(labels, values, color=colors)
        ax2.set_ylim(0, 100)
        ax2.set_ylabel("Score Level")
        ax2.set_title("AI Wellness Score Breakdown")

        for bar in bars:
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height + 2,
                     f'{int(height)}',
                     ha='center', va='bottom')

        st.pyplot(fig2)

    # -------- TAB 2 --------
    with tab2:
        st.subheader("Mental Health Intelligence")

        if stress_level == "High":
            st.error("High stress detected. Prioritize recovery.")
            st.write("• 10 minutes daily meditation")
            st.write("• Reduce multitasking")
            st.write("• Schedule digital detox")
        elif stress_level == "Medium":
            st.warning("Moderate stress. Improve balance.")
            st.write("• Weekly reflection journaling")
            st.write("• 30 mins daily exercise")
            st.write("• Deep breathing exercises")
        else:
            st.success("Low stress. Maintain your system.")
            st.write("• Continue structured routine")
            st.write("• Challenge yourself with growth goals")

        st.subheader("📚 Recommended Books For You")
        for book in book_suggestions:
            st.write("-", book)

        st.subheader("💬 Insight")
        st.info(quote)

    # -------- TAB 3 --------
    with tab3:
        st.subheader("Goal Focus Blueprint")

        if productivity_score < 40:
            st.write("• Start with 1 small daily habit.")
            st.write("• Focus on consistency over intensity.")
        elif productivity_score < 75:
            st.write("• Use time blocking.")
            st.write("• Remove 1 distraction daily.")
        else:
            st.write("• Enter deep work mode 2 hrs daily.")
            st.write("• Build mastery in 1 core skill.")

        st.subheader("7-Day Action Plan")
        weekly_plan = [
            "Day 1: Define your 30-day goal",
            "Day 2: Deep Work (2 hours)",
            "Day 3: Skill Practice",
            "Day 4: Fitness + Reflection",
            "Day 5: Productivity Sprint",
            "Day 6: Learn + Implement",
            "Day 7: Review & Reset"
        ]

        for day in weekly_plan:
            st.write("-", day)

    # -------- DOCX REPORT --------
    doc = Document()
    doc.add_heading("AI Adaptive Wellness Report", 0)
    doc.add_paragraph(f"Stress Level: {stress_level}")
    doc.add_paragraph(f"Productivity Score: {productivity_score}/100")
    doc.add_paragraph(f"Mental Balance Score: {mental_balance}/100")
    doc.add_paragraph("Recommended Books:")
    for book in book_suggestions:
        doc.add_paragraph(book, style="List Bullet")

    buffer = io.BytesIO()
    doc.save(buffer)

    if st.download_button(
        "⬇️ Download Smart Report (DOCX)",
        data=buffer.getvalue(),
        file_name="AI_Smart_Wellness_Report.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    ):
        st.balloons()




