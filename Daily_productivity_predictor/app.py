# app.py

import streamlit as st
import pandas as pd
import pickle
from docx import Document
import io
import random
import matplotlib.pyplot as plt
import numpy as np
import os

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="🧠 AI Wellness & Performance Analyzer",
    page_icon="🧠",
    layout="wide"
)

# ---------------- DARK BACKGROUND IMAGE ----------------
bg_image_url = "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=1950&q=80"  # Wellness / AI / Fitness theme
st.markdown(
    f"""
    <style>
    .stApp {{
        background: url({bg_image_url});
        background-size: cover;
        background-position: center;
        color: white;
    }}
    h1, h2, h3, h4, h5 {{
        color: #00F5FF;
    }}
    .stButton>button {{
        background-color: #08F7FE;
        color: black;
        font-weight: bold;
    }}
    .stTextInput>div>div>input {{
        color: black;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# ---------------- LOGIN SYSTEM ----------------
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

st.title("🧠 AI Wellness & Performance Analyzer")
st.markdown("### Login to Access Your Personalized Dashboard")

login_method = st.radio("Choose Login Method", ["Pattern Key Login", "Magic Key Login"])

if not st.session_state.logged_in:
    if login_method == "Pattern Key Login":
        st.write("Click the icons in correct order to login:")
        icons = ["🏋️‍♂️", "📚", "💻", "🥗", "🎯"]
        random.shuffle(icons)
        selected_icons = st.multiselect("Select icons in order", icons)
        if st.button("Login via Pattern"):
            # Correct pattern
            if selected_icons == ["💻","📚","🎯"]:
                st.session_state.logged_in = True
                st.success("✅ Logged in successfully via Pattern!")
            else:
                st.error("❌ Incorrect pattern. Try again.")

    elif login_method == "Magic Key Login":
        magic_key_input = st.text_input("Enter your Magic Key", type="password")
        if st.button("Login via Magic Key"):
            if magic_key_input == "AIWellness123":
                st.session_state.logged_in = True
                st.success("✅ Logged in successfully via Magic Key!")
            else:
                st.error("❌ Incorrect Magic Key. Try again.")

# ---------------- MAIN APP ----------------
if st.session_state.logged_in:

    # ---------------- LOAD MODEL ----------------
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    MODEL_PATH = os.path.join(BASE_DIR, "models", "productivity_model.pkl")
    LE_PATH = os.path.join(BASE_DIR, "models", "label_encoder.pkl")

    with open(MODEL_PATH, "rb") as f:
        model = pickle.load(f)

    with open(LE_PATH, "rb") as f:
        le = pickle.load(f)

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

    st.markdown("---")

    st.header("🎯 Career Direction")
    career_domain = st.selectbox(
        "Select Career Domain",
        ["Management", "IT & Data", "Government Exams", "Creative Field", "Entrepreneurship"]
    )
    career_niche = st.text_input("Specific Niche (Example: Data Science, MBA Finance, UPSC, UI/UX)")

    st.markdown("---")

    # ---------------- GENERATE REPORT ----------------
    if st.button("Generate Full AI Wellness Report"):
        st.balloons()

        # -------- PREDICTION --------
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

        bmi = weight / ((height / 100) ** 2)

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
        st.markdown(f"## 💬 Dear {name}, Here Is Your Detailed AI Analysis")

        colA, colB, colC = st.columns(3)
        colA.metric("Stress Level", stress_level)
        colB.metric("Productivity", f"{productivity_score}/100")
        colC.metric("Health Score", f"{health_score}/100")

        st.progress(productivity_score / 100)

        # ---------------- BAR GRAPH ----------------
        st.subheader("⏳ Weekly Time Distribution")
        weekly_data = {
            "Study": study_hours * 7,
            "Workout": physical_activity * 7,
            "Sleep": sleep_hours * 7
        }

        fig, ax = plt.subplots(figsize=(6,3), facecolor="#0E1117")
        ax.set_facecolor("#0E1117")
        ax.bar(weekly_data.keys(), weekly_data.values(),
               color=["#00F5FF", "#FF2E63", "#08F7FE"])
        ax.tick_params(colors="white")
        ax.set_ylabel("Hours", color="white")
        st.pyplot(fig)

        # ---------------- DETAILED DIET ----------------
        st.subheader("🥗 Detailed Nutrition Strategy")
        st.write("Goal: Stable energy, muscle recovery, and mental clarity.")

        if food_type == "Vegetarian":
            st.write("Breakfast: Oats + Milk + Almonds (Complex carbs + Protein)")
            st.write("Lunch: Dal + Brown Rice + Paneer (High protein vegetarian)")
            st.write("Evening: Fruits + Nuts (Micronutrients)")
            st.write("Dinner: Light roti + vegetables (Low fat)")
        elif food_type == "Vegan":
            st.write("Breakfast: Peanut butter smoothie (Plant protein)")
            st.write("Lunch: Quinoa + Chickpeas (Complete amino acids)")
            st.write("Snack: Seeds mix")
            st.write("Dinner: Tofu + Vegetables")
        else:
            st.write("Breakfast: Eggs + Whole wheat toast (High protein)")
            st.write("Lunch: Grilled chicken + Rice (Muscle repair)")
            st.write("Snack: Yogurt")
            st.write("Dinner: Fish + Salad (Omega-3 support)")

        # ---------------- DETAILED WORKOUT ----------------
        st.subheader("🏋 Structured Weekly Workout Plan")
        if workout_type == "Gym Training":
            st.write("Mon: Chest + Triceps (Compound lifts)")
            st.write("Tue: Back + Biceps")
            st.write("Wed: Legs (Heavy squats)")
            st.write("Thu: Shoulders")
            st.write("Fri: Core + HIIT")
        elif workout_type == "Home Workout":
            st.write("Pushups 3x15")
            st.write("Squats 3x20")
            st.write("Plank 3x60 sec")
            st.write("Jump rope 10 min")
        elif workout_type == "Yoga Only":
            st.write("Surya Namaskar 10 rounds")
            st.write("Pranayama 15 min")
            st.write("Meditation 20 min")
        elif workout_type == "Cardio Focus":
            st.write("Running 30 min")
            st.write("Cycling 20 min")
            st.write("HIIT 15 min")
        else:
            st.write("Strength 3 days")
            st.write("Cardio 2 days")
            st.write("Yoga 1 day")

        # ---------------- 90-DAY CAREER BLUEPRINT ----------------
        st.subheader("🚀 90-Day Career Execution Blueprint")
        st.write("Month 1: Build Core Knowledge")
        st.write("Week 1-2: Fundamentals")
        st.write("Week 3-4: Practice + Mini Project")

        st.write("Month 2: Advanced Skill + Major Project")
        st.write("Week 5-6: Deep specialization")
        st.write("Week 7-8: Build strong portfolio")

        st.write("Month 3: Execution")
        st.write("Week 9-10: Mock interviews")
        st.write("Week 11-12: Apply & network aggressively")

        # ---------------- FINAL MOTIVATION ----------------
        st.subheader("💬 Final Consultant Advice")
        st.markdown(f"""
Dear {name},

If you execute this plan consistently for 90 days in **{career_niche}**, 
your confidence, skill level, and opportunities will dramatically improve.

Momentum builds identity.
Identity builds success.
""")

        # ---------------- DOCX REPORT ----------------
        doc = Document()
        doc.add_heading("AI Wellness Report", 0)
        doc.add_paragraph(f"Name: {name}")
        doc.add_paragraph(f"Stress Level: {stress_level}")
        doc.add_paragraph(f"Productivity Score: {productivity_score}")
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
