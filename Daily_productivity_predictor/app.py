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
with open("models/productivity_model.pkl", "rb") as f:
    model = pickle.load(f)

with open("models/label_encoder.pkl", "rb") as f:
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
    food_type = st.selectbox(
        "Type of Food You Eat",
        ["Vegetarian", "Non-Vegetarian", "Vegan"]
    )
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

    # -------- ADVANCED SCORES --------
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

    # ---------------- DASHBOARD ----------------
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 AI Dashboard",
        "🏋️ Workout Plan",
        "🥗 Nutrition",
        "🧠 Mental Health",
        "📅 Weekly Growth Plan"
    ])

    # TAB 1
    with tab1:
        st.subheader("Stress Prediction")
        st.success(f"Predicted Stress Level: {stress_level}")
        st.write(f"BMI: {round(bmi,2)} ({bmi_status})")

        colA, colB = st.columns(2)

        with colA:
            st.metric("Productivity Score", f"{productivity_score}/100")
            st.progress(productivity_score / 100)

        with colB:
            st.metric("Health Score", f"{health_score}/100")
            st.progress(health_score / 100)

        st.subheader("Burnout Risk")
        if burnout_risk == "High":
            st.error("🚨 High Burnout Risk")
        elif burnout_risk == "Moderate":
            st.warning("⚠️ Moderate Burnout Risk")
        else:
            st.success("✅ Low Burnout Risk")

        # Radar Chart
        categories = ["Sleep", "Activity", "Stress", "Motivation", "Hydration"]
        values = [
            sleep_hours * 10,
            physical_activity * 20,
            100 - (career_stress * 10),
            motivation * 10,
            water * 20
        ]

        values += values[:1]
        angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=False).tolist()
        angles += angles[:1]

        fig, ax = plt.subplots(figsize=(6,6), subplot_kw=dict(polar=True))
        ax.plot(angles, values)
        ax.fill(angles, values, alpha=0.25)
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(categories)
        ax.set_yticklabels([])
        st.pyplot(fig)

    # TAB 2
    with tab2:
        st.subheader("Weekly Workout Plan")
        for w in workout_plan:
            st.write("-", w)

    # TAB 3
    with tab3:
        if want_diet == "Yes":
            st.subheader("⭐ Personalized Diet Plan")
            for d in personalized_diet:
                st.write("-", d)
        else:
            st.subheader("General Healthy Diet Plan")
            for d in general_diet:
                st.write("-", d)

    # TAB 4
    with tab4:
        st.subheader("Mental Health Suggestions")
        if career_stress > 7:
            st.write("• Practice daily meditation (10 mins)")
            st.write("• Use Pomodoro technique")
        if sleep_hours < 6:
            st.write("• Maintain fixed sleep schedule")
        if motivation < 5:
            st.write("• Break goals into smaller tasks")

    # TAB 5
    with tab5:
        st.subheader("7-Day Growth Plan")
        weekly_plan = [
            "Day 1: Plan goals & schedule",
            "Day 2: Deep work session",
            "Day 3: Cardio + Skill learning",
            "Day 4: Strength training",
            "Day 5: Focused productivity block",
            "Day 6: Reflection",
            "Day 7: Full rest"
        ]
        for day in weekly_plan:
            st.write("-", day)

    # ---------------- DOCX REPORT ----------------
    doc = Document()
    doc.add_heading("AI Wellness & Performance Report", 0)
    doc.add_paragraph(f"Stress Level: {stress_level}")
    doc.add_paragraph(f"BMI: {round(bmi,2)} ({bmi_status})")
    doc.add_paragraph(f"Productivity Score: {productivity_score}/100")
    doc.add_paragraph(f"Health Score: {health_score}/100")
    doc.add_paragraph(f"Burnout Risk: {burnout_risk}")

    doc.add_heading("Workout Plan", level=1)
    for w in workout_plan:
        doc.add_paragraph(w, style="List Bullet")

    doc.add_heading("Diet Plan", level=1)
    if want_diet == "Yes":
        for d in personalized_diet:
            doc.add_paragraph(d, style="List Bullet")
    else:
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

