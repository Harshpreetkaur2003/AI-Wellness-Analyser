# app.py

import streamlit as st
import pandas as pd
import pickle
from docx import Document
import io
import random
import numpy as np
import matplotlib.pyplot as plt
import os

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AI Wellness & Performance Analyzer",
    page_icon="🧠",
    layout="wide"
)

# ---------------- BACKGROUND + FONT ----------------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap');
    .stApp {
        background: url('https://images.unsplash.com/photo-1556761175-129418cb2dfe?auto=format&fit=crop&w=1950&q=80') no-repeat center center fixed;
        background-size: cover;
        font-family: 'Roboto', sans-serif;
        color: white;
    }
    h1, h2, h3 {
        color: #00F5FF;
        font-family: 'Roboto', sans-serif;
    }
    .glass {
        background: rgba(0,0,0,0.5);
        padding: 20px;
        border-radius: 15px;
        backdrop-filter: blur(8px);
        margin-bottom: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ---------------- LOGIN SYSTEM ----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.markdown("<h2>🔒 Login to Access AI Wellness App</h2>", unsafe_allow_html=True)
    login_method = st.radio("Choose Login Method", ["Magic Key", "Pattern Login"])

    # -------- Magic Key --------
    if login_method == "Magic Key":
        magic_input = st.text_input("Enter Your Magic Key", type="password")
        if st.button("Login via Magic Key"):
            if magic_input == "I conquer daily challenges":  # predefined magic key
                st.session_state.logged_in = True
                st.success("✅ Logged in successfully!")
            else:
                st.error("❌ Invalid Magic Key. Try again.")

    # -------- Captcha-Style Pattern Login --------
    if login_method == "Pattern Login":
        st.write("Click the icons in correct order to login:")
        icons = ["🏋️‍♂️","📚","💻","🥗","🎯"]
        random.shuffle(icons)
        selected_icons = st.multiselect("Select icons in order", icons)

        if st.button("Login via Pattern"):
            if selected_icons == ["💻","📚","🎯"]:  # predefined sequence
                st.session_state.logged_in = True
                st.success("✅ Logged in successfully!")
            else:
                st.error("❌ Incorrect pattern. Try again.")

    st.stop()  # stop execution until login

# ---------------- LOAD MODEL ----------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "models", "productivity_model.pkl")
LE_PATH = os.path.join(BASE_DIR, "models", "label_encoder.pkl")

with open(MODEL_PATH, "rb") as f:
    model = pickle.load(f)

with open(LE_PATH, "rb") as f:
    le = pickle.load(f)

# ---------------- APP TITLE ----------------
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

    # -------- ML Prediction --------
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
    productivity_score = int((sleep_hours * 10) + (physical_activity * 15) + (motivation * 5) - (career_stress * 4))
    productivity_score = max(0, min(productivity_score, 100))
    health_score = int((100 - abs(22 - bmi) * 5) + (physical_activity * 10) + (water * 5))
    health_score = max(0, min(health_score, 100))

    # ---------------- KPI CARDS ----------------
    st.markdown(f"## 💬 Dear {name}, Here Is Your Detailed AI Analysis")
    colA, colB, colC = st.columns(3)
    colA.metric("Stress Level", stress_level)
    colB.metric("Productivity Score", f"{productivity_score}/100")
    colC.metric("Health Score", f"{health_score}/100")

    st.progress(productivity_score / 100)

    # ---------------- TABS ----------------
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Analytics",
        "🥗 Diet & Workout",
        "🧠 Consultant Report",
        "🎯 Career Blueprint"
    ])

    # ---------------- TAB 1: Analytics ----------------
    with tab1:
        st.subheader("⏳ Weekly Time Distribution")
        weekly_data = {
            "Study": study_hours * 7,
            "Workout": physical_activity * 7,
            "Sleep": sleep_hours * 7
        }
        fig, ax = plt.subplots(figsize=(6,3), facecolor='lightgray')
        ax.set_facecolor("lightgray")
        ax.bar(weekly_data.keys(), weekly_data.values(), color=["#00F5FF", "#FF2E63", "#08F7FE"])
        ax.tick_params(colors="black")
        ax.set_ylabel("Hours", color="black")
        st.pyplot(fig)

        st.subheader("📊 Overall Performance Radar")
        categories = ["Sleep", "Workout", "Motivation", "Study"]
        values = [
            sleep_hours / 12,
            physical_activity / 4,
            motivation / 10,
            study_hours / 12
        ]
        angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=False)
        values += values[:1]
        angles = np.concatenate((angles, [angles[0]]))
        fig2, ax2 = plt.subplots(figsize=(4,4), subplot_kw=dict(polar=True))
        fig2.patch.set_facecolor("lightgray")
        ax2.set_facecolor("lightgray")
        ax2.plot(angles, values, color="#00F5FF")
        ax2.fill(angles, values, color="#00F5FF", alpha=0.3)
        ax2.set_xticks(angles[:-1])
        ax2.set_xticklabels(categories, color="black")
        ax2.set_yticklabels([])
        st.pyplot(fig2)

    # ---------------- TAB 2: Diet & Workout ----------------
    with tab2:
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

    # ---------------- TAB 3: Consultant Report ----------------
    with tab3:
        st.subheader("💬 Mental & Productivity Guidance")
        st.write(f"Predicted Stress Level: {stress_level}")
        st.write(f"Productivity Score: {productivity_score}/100")
        st.write(f"Health Score: {health_score}/100")
        st.write("• Maintain healthy sleep and workout routine")
        st.write("• Track water intake daily")
        st.write("• Schedule breaks to reduce stress")

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

    # ---------------- TAB 4: Career Blueprint ----------------
    with tab4:
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
