# app.py

import streamlit as st
import pandas as pd
import pickle
from docx import Document
import io
import os
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AI Wellness & Performance Analyzer",
    page_icon="🧠",
    layout="wide"
)

# ---------------- PREMIUM GRADIENT DARK UI ----------------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
    color: white;
}
h1, h2, h3 {
    color: #00F5FF;
}
div[data-testid="stMetricValue"] {
    color: #00F5FF;
}
</style>
""", unsafe_allow_html=True)

st.title("🧠 AI Wellness & Performance Analyzer")
st.markdown("### Smart Lifestyle • Stress Prediction • Fitness • Career Blueprint")
st.markdown("---")

# ---------------- LOAD MODEL ----------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(BASE_DIR, "models", "productivity_model.pkl")
LE_PATH = os.path.join(BASE_DIR, "models", "label_encoder.pkl")

with open(MODEL_PATH, "rb") as f:
    model = pickle.load(f)

with open(LE_PATH, "rb") as f:
    le = pickle.load(f)

# ---------------- TABS ----------------
tab1, tab2, tab3 = st.tabs(["📋 Input", "📊 Analytics", "📄 Report"])

# ---------------- INPUT TAB ----------------
with tab1:

    st.header("Enter Your Details")

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

    career_domain = st.selectbox(
        "Select Career Domain",
        ["Management", "IT & Data", "Government Exams", "Creative Field", "Entrepreneurship"]
    )

    career_niche = st.text_input("Specific Niche (Example: Data Science, MBA Finance, UPSC)")

    generate = st.button("Generate Full AI Report")

# ---------------- PROCESS LOGIC ----------------
if generate:

    st.balloons()

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

    # ---------------- ANALYTICS TAB ----------------
    with tab2:

        st.header(f"Dear {name}, Here Is Your Performance Dashboard")

        colA, colB, colC = st.columns(3)
        colA.metric("Stress Level", stress_level)
        colB.metric("Productivity", f"{productivity_score}/100")
        colC.metric("Health Score", f"{health_score}/100")

        st.markdown("---")

        # INTERACTIVE BAR GRAPH
        fig_bar = go.Figure()

        fig_bar.add_trace(go.Bar(
            x=["Productivity", "Health"],
            y=[productivity_score, health_score],
            text=[productivity_score, health_score],
            textposition="auto"
        ))

        fig_bar.update_layout(
            template="plotly_dark",
            height=400,
            title="Overall Score Comparison"
        )

        st.plotly_chart(fig_bar, use_container_width=True)

        # 3D GRAPH
        fig_3d = go.Figure(data=[go.Scatter3d(
            x=[sleep_hours],
            y=[study_hours],
            z=[productivity_score],
            mode='markers',
            marker=dict(
                size=10,
                color=productivity_score,
                colorscale='Viridis'
            )
        )])

        fig_3d.update_layout(
            template="plotly_dark",
            height=500,
            scene=dict(
                xaxis_title="Sleep Hours",
                yaxis_title="Study Hours",
                zaxis_title="Productivity Score"
            ),
            title="3D Lifestyle Impact View"
        )

        st.plotly_chart(fig_3d, use_container_width=True)

    # ---------------- REPORT TAB ----------------
    with tab3:

        st.header("Detailed Consultant Report")

        st.subheader("🥗 Nutrition Plan")

        if food_type == "Vegetarian":
            st.write("High protein vegetarian structure with paneer, lentils, oats.")
        elif food_type == "Vegan":
            st.write("Plant protein rotation with tofu, quinoa, seeds.")
        else:
            st.write("Lean protein cycle: eggs, chicken, fish with controlled carbs.")

        st.subheader("🏋 Weekly Workout Plan")

        if workout_type == "Gym Training":
            st.write("Push-Pull-Legs split with progressive overload.")
        elif workout_type == "Home Workout":
            st.write("Bodyweight hypertrophy + core focus.")
        elif workout_type == "Yoga Only":
            st.write("Flexibility + breath control + mindfulness.")
        elif workout_type == "Cardio Focus":
            st.write("Fat loss + endurance training model.")
        else:
            st.write("Hybrid strength + conditioning.")

        st.subheader("🚀 90 Day Career Blueprint")

        st.write("Month 1: Fundamentals")
        st.write("Month 2: Advanced Skill + Project")
        st.write("Month 3: Execution + Applications")

        st.markdown(f"""
Dear {name},

If you stay consistent in **{career_niche}**, your growth will compound daily.

Discipline beats motivation.
Execution beats planning.
Consistency builds identity.
""")

        # DOCX DOWNLOAD
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
            "Download Professional Report",
            data=buffer.getvalue(),
            file_name="AI_Wellness_Report.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
