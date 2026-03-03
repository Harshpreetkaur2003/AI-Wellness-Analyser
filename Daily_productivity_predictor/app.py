# app.py

import streamlit as st
import pandas as pd
import pickle
from docx import Document
import io
import random
import numpy as np
import plotly.graph_objects as go
import os
import string

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AI Wellness & Performance Analyzer",
    page_icon="🧠",
    layout="wide"
)

# ---------------- CINEMATIC NOIR BACKGROUND ----------------
st.markdown(
    """
    <style>
    .stApp {
        background: url('https://images.unsplash.com/photo-1518709268802-4c3e7b9e13d7?auto=format&fit=crop&w=1950&q=80') no-repeat center center fixed;
        background-size: cover;
        color: white;
        font-family: 'Segoe UI', sans-serif;
    }
    h1, h2, h3 {
        color: #00F5FF;
        font-weight: 700;
        text-shadow: 2px 2px 8px #000000;
    }
    .glass {
        background: rgba(0,0,0,0.7);
        padding: 20px;
        border-radius: 20px;
        backdrop-filter: blur(20px);
        margin-bottom: 20px;
        box-shadow: 0 0 15px #000000;
    }
    .metric-box {
        background: rgba(0,0,0,0.75);
        border-radius: 15px;
        padding: 15px;
        text-align: center;
        box-shadow: 0 0 10px #111111;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ---------------- SESSION STATE ----------------
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False



# ---------------- LOGIN ----------------
if not st.session_state.authenticated:
    st.title("🔐 Secure Access Portal")
    login_type = st.radio("Choose Authentication Method", ["Secret Passphrase", "Dynamic OTP Login"])

    if login_type == "Secret Passphrase":
        passphrase = st.text_input("Enter Secret Passphrase", type="password")
        if st.button("Login"):
            if passphrase == "UnlockMyWellnessAI":
                st.session_state.authenticated = True
                st.success("✅ Access Granted!")
                st.rerun()
            else:
                st.error("❌ Incorrect Passphrase")

    elif login_type == "Dynamic OTP Login":
        st.info(f"Your One-Time Code: {st.session_state.generated_otp}")
        otp_input = st.text_input("Enter the OTP above")
        if st.button("Verify OTP"):
            if otp_input == st.session_state.generated_otp:
                st.session_state.authenticated = True
                st.success("✅ OTP Verified! Access Granted.")
                st.rerun()
            else:
                st.error("❌ Invalid OTP")

    st.stop()

# ---------------- APP TITLE ----------------
st.markdown('<div class="glass"><h1>🧠 AI Wellness & Performance Analyzer</h1></div>', unsafe_allow_html=True)
st.markdown('<div class="glass"><h3>Smart Lifestyle • Stress Prediction • Fitness • Career Blueprint</h3></div>', unsafe_allow_html=True)



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

    # ML Prediction
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

    # KPI Metrics
    bmi = weight / ((height / 100) ** 2)
    productivity_score = max(0, min(int((sleep_hours * 10) + (physical_activity * 15) + (motivation * 5) - (career_stress * 4)), 100))
    health_score = max(0, min(int((100 - abs(22 - bmi) * 5) + (physical_activity * 10) + (water * 5)), 100))

    st.markdown(f'<div class="glass"><h2>💬 Dear {name}, Here Is Your Detailed AI Analysis</h2></div>', unsafe_allow_html=True)
    colA, colB, colC = st.columns(3)
    colA.metric("Stress Level", stress_level)
    colB.metric("Productivity Score", f"{productivity_score}/100")
    colC.metric("Health Score", f"{health_score}/100")

    st.progress(productivity_score / 100)

    # ---------------- TABS ----------------
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Analytics","🥗 Diet & Workout","🧠 Consultant Report","🎯 Career Blueprint"])

    # ---------------- TAB 1: Analytics ----------------
    with tab1:
        st.subheader("📈 Lifestyle & Performance Overview")
        factors = ["Sleep","Workout","Motivation","Stress Impact"]
        values = [sleep_hours*10, physical_activity*15, motivation*5, -career_stress*4]
        fig_combo = go.Figure()
        fig_combo.add_trace(go.Bar(x=factors, y=values, name="Impact Contribution", marker_color="#00F5FF"))
        fig_combo.add_trace(go.Scatter(x=factors, y=np.cumsum(values), mode="lines+markers", name="Cumulative Effect", line=dict(color="#FF2E63")))
        fig_combo.update_layout(template="plotly_dark", height=400, title="Factor Contribution & Cumulative Curve")
        st.plotly_chart(fig_combo, use_container_width=True)

        # Donut chart
        st.subheader("⚖ Daily Life Balance")
        balance_data = {"Study": study_hours,"Sleep": sleep_hours,"Workout": physical_activity,"Social": social_hours}
        fig_donut = go.Figure(data=[go.Pie(labels=list(balance_data.keys()), values=list(balance_data.values()), hole=0.6)])
        fig_donut.update_layout(template="plotly_dark", height=400, title="Daily Balance Ratio")
        st.plotly_chart(fig_donut, use_container_width=True)

        # 3D Surface
        st.subheader("🧠 Predictive 3D Performance Surface")
        x = np.linspace(4,10,20)
        y = np.linspace(1,6,20)
        X,Y = np.meshgrid(x,y)
        Z = (X*8)+(Y*12)
        fig_surface = go.Figure(data=[go.Surface(z=Z,x=X,y=Y)])
        fig_surface.update_layout(template="plotly_dark", height=500, scene=dict(xaxis_title="Sleep Hours", yaxis_title="Workout Hours", zaxis_title="Performance Potential"), title="Lifestyle-Performance Simulation")
        st.plotly_chart(fig_surface,use_container_width=True)

    # ---------------- TAB 2: Diet & Workout ----------------
    with tab2:
        st.subheader("🥗 Personalized Nutrition")
        if food_type=="Vegetarian":
            st.write("Breakfast: Oats + Milk + Almonds\nLunch: Dal + Brown Rice + Paneer\nEvening: Fruits + Nuts\nDinner: Light Roti + Vegetables")
        elif food_type=="Vegan":
            st.write("Breakfast: Peanut Butter Smoothie\nLunch: Quinoa + Chickpeas\nSnack: Seeds Mix\nDinner: Tofu + Vegetables")
        else:
            st.write("Breakfast: Eggs + Toast\nLunch: Grilled Chicken + Rice\nSnack: Yogurt\nDinner: Fish + Salad")

        st.subheader("🏋 Structured Weekly Workout Plan")
        if workout_type=="Gym Training":
            st.write("Mon: Chest + Triceps\nTue: Back + Biceps\nWed: Legs\nThu: Shoulders\nFri: Core + HIIT")
        elif workout_type=="Home Workout":
            st.write("Pushups 3x15\nSquats 3x20\nPlank 3x60 sec\nJump Rope 10 min")
        elif workout_type=="Yoga Only":
            st.write("Surya Namaskar 10 rounds\nPranayama 15 min\nMeditation 20 min")
        elif workout_type=="Cardio Focus":
            st.write("Running 30 min\nCycling 20 min\nHIIT 15 min")
        else:
            st.write("Strength 3 days\nCardio 2 days\nYoga 1 day")

    # ---------------- TAB 3: Consultant Report ----------------
    with tab3:
        st.subheader("🧠 Detailed Consultant Analysis")
        st.write(f"Dear {name}, based on your inputs and lifestyle metrics:")
        st.markdown("**Stress Analysis:**")
        st.write("High stress! Prioritize recovery cycles." if career_stress>7 else "Moderate stress, manageable with discipline." if career_stress>4 else "Healthy stress zone, keep it balanced.")
        st.markdown("**Productivity Deep Dive:**")
        st.write(f"- Sleep Contribution: {sleep_hours*10}\n- Workout Contribution: {physical_activity*15}\n- Motivation Contribution: {motivation*5}\n- Stress Deduction: {-career_stress*4}")
        st.markdown("**Nutrition Advice:**")
        st.write(f"{food_type} diet optimized for mental clarity, energy, and muscle recovery.")
        st.markdown("**Workout Guidance:**")
        st.write(f"{workout_type} routine structured for max performance and recovery.")
        st.markdown("**Motivational Quote:**")
        quotes=["Small daily improvements lead to stunning long-term results.","Discipline creates freedom.","Your future is created by what you do today.","Focus on progress, not perfection."]
        st.info(random.choice(quotes))

    # ---------------- TAB 4: Career Blueprint ----------------
    with tab4:
        st.subheader("🎯 90-Day Career Execution Plan")
        st.write(f"Domain: {career_domain}\nSpecialization: {career_niche}")
        st.write("Month 1 → Skill Foundation & Concept Clarity\nMonth 2 → Portfolio / Practical Exposure\nMonth 3 → Mock Testing + Real Applications")
        st.write("Weekly: 5 Days Skill Deep Work, 1 Day Review, 1 Day Reflection + Networking")

    # ---------------- REPORT DOWNLOAD ----------------
    doc = Document()
    doc.add_heading("AI Wellness & Career Report", 0)
    doc.add_paragraph(f"Name: {name}")
    doc.add_paragraph(f"Stress Level: {stress_level}")
    doc.add_paragraph(f"Productivity Score: {productivity_score}")
    doc.add_paragraph(f"Health Score: {health_score}")
    doc.add_paragraph(f"Career Domain: {career_domain}")
    doc.add_paragraph(f"Career Niche: {career_niche}")

    buffer = io.BytesIO()
    doc.save(buffer)
    st.download_button("⬇️ Download Full Professional Report", data=buffer.getvalue(),
                       file_name="AI_Wellness_Report.docx",
                       mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")



