# app.py

import streamlit as st
import pandas as pd
import pickle
from docx import Document
import io
import matplotlib.pyplot as plt

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
    page_title="AI Lifestyle & Career Consultant",
    page_icon="🧠",
    layout="wide"
)

st.title("🧠 AI Lifestyle & Career Consultant")
st.markdown("### Personalized Growth. Structured Strategy. Real Results.")
st.markdown("---")

# ---------------- INPUT SECTION ----------------
st.header("📋 Tell Me About Yourself")

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

    diet_type = st.selectbox(
        "Your Diet Preference",
        ["Vegetarian", "Non-Vegetarian", "Vegan"]
    )

    workout_goal = st.selectbox(
        "Preferred Workout Goal",
        ["Weight Loss", "Muscle Gain", "General Fitness", "Stress Relief"]
    )

    excel_field = st.selectbox(
        "Field You Want To Excel In",
        ["AI/ML", "Coding", "Business", "Academics", "Public Speaking", "Fitness"]
    )

st.markdown("---")

# ---------------- BUTTON ----------------
if st.button("Generate My Personalized Consultant Report"):

    st.balloons()
    st.success("🎉 Your Personalized AI Consultant Report is Ready!")

    # ---------------- PREDICTION ----------------
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

    # ---------------- BMI ----------------
    bmi = weight / ((height / 100) ** 2)

    if bmi < 18.5:
        bmi_status = "Underweight"
    elif bmi < 24.9:
        bmi_status = "Normal"
    elif bmi < 29.9:
        bmi_status = "Overweight"
    else:
        bmi_status = "Obese"

    # ---------------- SCORES ----------------
    productivity_score = max(0, min(int(
        (sleep_hours * 10) +
        (physical_activity * 15) +
        (motivation * 6) -
        (career_stress * 5)
    ), 100))

    mental_balance = max(0, min(int(
        (sleep_hours * 12) +
        (water * 8) -
        (career_stress * 6)
    ), 100))

    burnout_risk = career_stress * 10 - sleep_hours * 5

    # ---------------- CONSULTANT MESSAGE ----------------
    st.header("💬 Personal Consultant Message")

    st.write(f"Dear {name if name else 'Champion'},")
    st.write("""
I’ve carefully analyzed your habits, stress levels, physical activity,
and career ambitions. Below is your structured 90-day optimization plan.
Let’s improve your life strategically — not randomly.
""")

    st.markdown("---")

    # ---------------- HEALTH ANALYSIS ----------------
    st.subheader("🩺 Health Analysis")

    st.write(f"• BMI: **{round(bmi,2)} ({bmi_status})**")
    st.write(f"• Predicted Stress Level: **{stress_level}**")
    st.write(f"• Productivity Score: **{productivity_score}/100**")
    st.write(f"• Mental Balance Score: **{mental_balance}/100**")

    if burnout_risk > 50:
        st.error("⚠ I’m concerned. Your burnout risk is high. Recovery must be prioritized.")

    # ---------------- DIET PLAN ----------------
    st.subheader("🥗 Structured Diet Plan")

    if diet_type == "Vegetarian":
        diet_plan = """
Morning: Warm water + soaked almonds  
Breakfast: Oats / Paneer + roti  
Lunch: Dal + 2 roti + sabzi + salad  
Evening: Green tea + roasted chana  
Dinner: Light khichdi / paneer bhurji  
Avoid fried & excess sugar  
"""
    elif diet_type == "Non-Vegetarian":
        diet_plan = """
Breakfast: Eggs + brown bread  
Lunch: Grilled chicken/fish + rice + veggies  
Evening: Fruit + nuts  
Dinner: Soup + boiled eggs  
Maintain high protein intake  
"""
    else:
        diet_plan = """
Breakfast: Smoothie (banana + peanut butter + soy milk)  
Lunch: Brown rice + tofu + veggies  
Evening: Mixed seeds  
Dinner: Lentil soup + salad  
Ensure B12 supplementation  
"""

    st.write(diet_plan)

    # ---------------- WORKOUT PLAN ----------------
    st.subheader("🏋 Structured Weekly Workout Plan")

    if workout_goal == "Weight Loss":
        workout_plan = """
5 days brisk walking (30 mins)  
3 days bodyweight circuit training  
1 day stretching  
"""
    elif workout_goal == "Muscle Gain":
        workout_plan = """
Day 1: Chest & Triceps  
Day 2: Back & Biceps  
Day 3: Legs  
Progressive overload weekly  
Protein 1.5g per kg body weight  
"""
    elif workout_goal == "Stress Relief":
        workout_plan = """
Daily 20 mins yoga  
Breathing exercises morning & night  
Evening phone-free walk  
"""
    else:
        workout_plan = """
3x Full body workout  
2x Cardio  
1x Mobility training  
"""

    st.write(workout_plan)

    # ---------------- CAREER ROADMAP ----------------
    st.subheader("🚀 90-Day Career Roadmap")

    if excel_field == "AI/ML":
        roadmap = """
Weeks 1–4: Strengthen Python, Numpy, Pandas  
Weeks 5–8: Build 2 ML projects  
Weeks 9–12: Deploy app + Kaggle participation  
Weekly Time: 15–20 hours  
"""
    elif excel_field == "Coding":
        roadmap = """
Weeks 1–4: DSA basics (Arrays, Recursion)  
Weeks 5–8: Trees, Graphs, Mock Interviews  
Weeks 9–12: Full-stack project deployment  
Weekly Time: 12–15 hours  
"""
    elif excel_field == "Business":
        roadmap = """
Weeks 1–4: Marketing fundamentals  
Weeks 5–8: Start small online project  
Weeks 9–12: Analyze metrics & optimize  
Weekly Time: 10–15 hours  
"""
    else:
        roadmap = """
Phase 1: Skill Building  
Phase 2: Real-world application  
Phase 3: Optimization & consistency  
"""

    st.write(roadmap)

    # ---------------- WEEKLY TIME CHART ----------------
    st.subheader("⏳ Weekly Preparation Time Allocation")

    time_data = {
        "Skill Practice": 8,
        "Project Work": 5,
        "Revision": 3,
        "Networking": 2
    }

    fig, ax = plt.subplots()
    ax.bar(time_data.keys(), time_data.values())
    ax.set_ylabel("Hours per Week")
    st.pyplot(fig)

    # ---------------- LIFESTYLE SCORE CHART ----------------
    st.subheader("📊 Lifestyle Score Overview")

    scores = {
        "Productivity": productivity_score,
        "Mental Balance": mental_balance,
        "Fitness": physical_activity * 25
    }

    fig2, ax2 = plt.subplots()
    ax2.bar(scores.keys(), scores.values())
    ax2.set_ylim(0, 100)
    st.pyplot(fig2)

    # ---------------- FINAL MOTIVATION ----------------
    st.markdown("---")
    st.subheader("💡 Final Message")

    if productivity_score > 75:
        final_quote = "You’re operating at high potential. Now execute with discipline."
    elif stress_level == "High":
        final_quote = "Growth is powerful, but balance is wisdom. Protect your energy."
    else:
        final_quote = "Consistency beats intensity. Show up daily."

    st.info(f"✨ {final_quote}")

    # ---------------- DOCX REPORT ----------------
    doc = Document()
    doc.add_heading("AI Personalized Consultant Report", 0)
    doc.add_paragraph(f"Name: {name}")
    doc.add_paragraph(f"Stress Level: {stress_level}")
    doc.add_paragraph(f"BMI: {round(bmi,2)} ({bmi_status})")
    doc.add_paragraph("Diet Plan:")
    doc.add_paragraph(diet_plan)
    doc.add_paragraph("Workout Plan:")
    doc.add_paragraph(workout_plan)
    doc.add_paragraph("Career Roadmap:")
    doc.add_paragraph(roadmap)
    doc.add_paragraph(f"Final Motivation: {final_quote}")

    buffer = io.BytesIO()
    doc.save(buffer)

    st.download_button(
        "⬇ Download Full Consultant Report",
        data=buffer.getvalue(),
        file_name="AI_Consultant_Report.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )


