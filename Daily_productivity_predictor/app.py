import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from docx import Document
import random

st.set_page_config(page_title="AI Wellness & Career Consultant", layout="wide")
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(BASE_DIR, "models", "productivity_model.pkl")
LE_PATH = os.path.join(BASE_DIR, "models", "label_encoder.pkl")

with open(MODEL_PATH, "rb") as f:
    model = pickle.load(f)

with open(LE_PATH, "rb") as f:
    le = pickle.load(f)

# -------------------- PREMIUM UI --------------------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #141E30, #243B55, #1c1c1c);
    background-attachment: fixed;
}

h1, h2, h3, h4, h5, h6, p, label {
    color: #f5f5f5 !important;
}

[data-testid="metric-container"] {
    background-color: rgba(255, 255, 255, 0.08);
    border-radius: 12px;
    padding: 15px;
}

.stButton>button {
    background: linear-gradient(45deg, #00c6ff, #0072ff);
    color: white;
    border-radius: 8px;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# -------------------- HEADER --------------------
st.title("🧠 AI Wellness & Career Consultant")

st.image(
    "https://images.unsplash.com/photo-1519389950473-47ba0277781c",
    use_column_width=True
)

st.markdown("---")

# -------------------- USER INPUT --------------------
name = st.text_input("Enter Your Name")
age = st.number_input("Enter Age", 16, 60)
sleep_hours = st.slider("Sleep Hours", 0, 12)
study_hours = st.slider("Study/Work Hours", 0, 12)
workout_hours = st.slider("Workout Hours", 0, 4)
water = st.slider("Water Intake (Litres)", 0.0, 5.0)
motivation = st.slider("Motivation Level (1-10)", 1, 10)

diet_type = st.selectbox("Diet Preference", ["Vegetarian", "Vegan", "Non-Vegetarian"])
workout_type = st.selectbox("Workout Type", ["Fat Loss", "Muscle Gain", "General Fitness"])

career_domain = st.selectbox(
    "Career Domain",
    ["IT", "Management", "Finance", "Entrepreneurship", "Creative Field"]
)

niche = st.text_input("Select / Enter Your Niche (Example: AI, Marketing, Investment Banking, Startup etc.)")

st.markdown("---")

# -------------------- CALCULATIONS --------------------
productivity_score = min(100, (sleep_hours*5 + study_hours*6 + motivation*4))
health_score = min(100, (sleep_hours*6 + workout_hours*15 + water*5))

# -------------------- METRICS --------------------
col1, col2 = st.columns(2)
col1.metric("⚡ Productivity Score", f"{productivity_score}/100")
col2.metric("💪 Health Score", f"{health_score}/100")

st.progress(productivity_score / 100)
st.progress(health_score / 100)

st.markdown("---")

# -------------------- DETAILED CONSULTANT SUGGESTIONS --------------------
if name:

    st.subheader("🩺 Personalized Consultant Advice")

    st.write(f"Dear {name}, based on your inputs, here’s my honest professional guidance for you:")

    # Sleep
    if sleep_hours < 6:
        st.warning("⚠ Your sleep is critically low. You must target 7-8 hours. Without recovery, productivity will crash.")
    else:
        st.success("✅ Good sleep habit. Maintain consistent sleep timing.")

    # Diet
    st.subheader("🥗 Detailed Diet Plan")

    if diet_type == "Vegetarian":
        st.write("""
- Breakfast: Oats + Peanut Butter + Banana  
- Lunch: Dal, Brown Rice, Paneer, Salad  
- Evening: Dry Fruits + Green Tea  
- Dinner: Roti + Mixed Veg + Curd  
- Protein Target: 1.0–1.2g per kg bodyweight
""")

    elif diet_type == "Vegan":
        st.write("""
- Breakfast: Smoothie (Almond Milk + Banana + Chia Seeds)  
- Lunch: Quinoa + Chickpeas + Tofu  
- Evening: Nuts + Coconut Water  
- Dinner: Lentils + Stir Fried Vegetables  
- Add B12 Supplement weekly
""")

    else:
        st.write("""
- Breakfast: Eggs + Toast + Fruits  
- Lunch: Chicken/Fish + Rice + Veggies  
- Evening: Boiled Eggs or Greek Yogurt  
- Dinner: Light Protein + Salad  
- Protein Target: 1.2–1.5g per kg bodyweight
""")

    # Workout Plan
    st.subheader("🏋 Customized Workout Plan")

    if workout_type == "Fat Loss":
        st.write("""
Weekly Plan:
Mon: Cardio + Core  
Tue: Lower Body Strength  
Wed: HIIT  
Thu: Upper Body  
Fri: Cardio  
Sat: Full Body Circuit  
Sun: Active Rest
""")
    elif workout_type == "Muscle Gain":
        st.write("""
Weekly Plan:
Mon: Chest + Triceps  
Tue: Back + Biceps  
Wed: Legs  
Thu: Shoulders  
Fri: Push-Pull Combo  
Sat: Light Cardio  
Sun: Rest
""")
    else:
        st.write("""
Weekly Plan:
3 Days Strength Training  
2 Days Cardio  
1 Day Yoga  
1 Day Rest
""")

    # Career Roadmap
    st.subheader("🚀 12-Week Career Roadmap")

    st.write(f"Target Domain: {career_domain} | Niche: {niche}")

    st.write("""
Weeks 1–4:
- Build fundamentals
- Study 2 hours daily
- Take 1 small project

Weeks 5–8:
- Build 2 major projects
- Improve LinkedIn
- Start networking

Weeks 9–12:
- Mock interviews
- Apply for internships/jobs
- Build portfolio website
""")

    st.markdown("---")

    # Graph Section
    st.subheader("📊 Performance Analytics")

    colg1, colg2 = st.columns(2)

    with colg1:
        fig, ax = plt.subplots(figsize=(4,3))
        ax.bar(["Productivity", "Health"], [productivity_score, health_score])
        ax.set_facecolor("#1f2c3c")
        fig.patch.set_facecolor("#1f2c3c")
        ax.tick_params(colors='white')
        ax.spines[:].set_color("white")
        ax.set_title("Score Comparison", color="white")
        st.pyplot(fig)

    with colg2:
        fig2, ax2 = plt.subplots(figsize=(4,3))
        ax2.plot(
            ["Sleep", "Study", "Workout", "Water"],
            [sleep_hours, study_hours, workout_hours, water],
            marker='o'
        )
        ax2.set_facecolor("#1f2c3c")
        fig2.patch.set_facecolor("#1f2c3c")
        ax2.tick_params(colors='white')
        ax2.spines[:].set_color("white")
        ax2.set_title("Habit Analysis", color="white")
        st.pyplot(fig2)

    st.markdown("---")

    # REPORT GENERATION
    if st.button("📄 Generate AI Report"):
        st.balloons()

        doc = Document()
        doc.add_heading("AI Wellness & Career Report", 0)
        doc.add_paragraph(f"Name: {name}")
        doc.add_paragraph(f"Productivity Score: {productivity_score}")
        doc.add_paragraph(f"Health Score: {health_score}")
        doc.add_paragraph("Diet Plan and Workout Plan included.")
        doc.save("AI_Report.docx")

        st.success("Report Generated Successfully!")

        quotes = [
            "Discipline beats motivation.",
            "Your future is created by what you do today.",
            "Consistency builds greatness."
        ]

        st.subheader("🔥 Final Motivation")
        st.write(random.choice(quotes))






