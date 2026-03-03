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

# ---------------- GENERATE REPORT ----------------
if st.button("Generate Smart AI Report"):

    # 🎈 Celebration Animation
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

    # -------- Dynamic Quote --------
    if stress_level == "High":
        quote = "Slow down. Recovery is also productivity."
    elif motivation < 5:
        quote = "Action creates motivation."
    elif productivity_score > 75:
        quote = "Mastery demands focus."
    else:
        quote = "Progress, not perfection."

    # ---------------- DASHBOARD ----------------
    st.header("📊 Performance Overview")

    colA, colB, colC = st.columns(3)

    colA.metric("Stress Level", stress_level)
    colB.metric("Productivity Score", f"{productivity_score}/100")
    colC.metric("Mental Balance", f"{mental_balance}/100")

    st.markdown("---")

    # -------- BAR GRAPH --------
    st.subheader("📊 Statistical Breakdown")

    labels = ["Sleep", "Activity", "Stress Control", "Motivation", "Hydration"]
    values = [
        sleep_hours * 10,
        physical_activity * 20,
        100 - (career_stress * 10),
        motivation * 10,
        water * 20
    ]

    fig1 = plt.figure()
    plt.bar(labels, values)
    plt.xticks(rotation=45)
    plt.ylabel("Score (0-100)")
    plt.title("Lifestyle Statistics Overview")
    st.pyplot(fig1)

    st.markdown("---")

    # -------- RADAR CHART --------
    st.subheader("📈 Performance Radar Chart")

    categories = ["Sleep", "Activity", "Stress", "Motivation"]
    radar_values = [
        sleep_hours * 10,
        physical_activity * 20,
        100 - (career_stress * 10),
        motivation * 10
    ]

    radar_values += radar_values[:1]
    angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=False).tolist()
    angles += angles[:1]

    fig2, ax = plt.subplots(subplot_kw=dict(polar=True))
    ax.plot(angles, radar_values)
    ax.fill(angles, radar_values, alpha=0.25)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories)
    ax.set_yticklabels([])

    st.pyplot(fig2)

    st.markdown("---")

    # -------- INSIGHT SECTION --------
    st.subheader("🧠 AI Insight")
    st.info(quote)

    # -------- DOCX REPORT --------
    doc = Document()
    doc.add_heading("AI Adaptive Wellness Report", 0)
    doc.add_paragraph(f"Stress Level: {stress_level}")
    doc.add_paragraph(f"BMI: {round(bmi,2)} ({bmi_status})")
    doc.add_paragraph(f"Productivity Score: {productivity_score}/100")
    doc.add_paragraph(f"Mental Balance Score: {mental_balance}/100")
    doc.add_paragraph(f"AI Insight: {quote}")

    buffer = io.BytesIO()
    doc.save(buffer)

    st.download_button(
        "⬇️ Download Smart Report (DOCX)",
        data=buffer.getvalue(),
        file_name="AI_Smart_Wellness_Report.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )



