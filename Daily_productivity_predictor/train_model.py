# train_model.py

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix
import pickle
import os

# -------- 1. Load dataset --------
data_path = "data/student_lifestyle_dataset.csv"  # Update if your CSV has a different name
df = pd.read_csv(data_path)

print("Dataset shape:", df.shape)
print("Columns:", df.columns)

# -------- 2. Handle missing values --------
df = df.dropna()  # Simple drop, optional: advanced imputation

# -------- 3. Choose features and target --------
target = "Stress_Level"  # Correct column from your dataset

# Features (excluding Student_ID and target)
features = [
    "Study_Hours_Per_Day",
    "Extracurricular_Hours_Per_Day",
    "Sleep_Hours_Per_Day",
    "Social_Hours_Per_Day",
    "Physical_Activity_Hours_Per_Day",
    "GPA"
]

# -------- 4. Encode target if it's categorical --------
le_target = LabelEncoder()
df[target] = le_target.fit_transform(df[target])  # Converts High/Medium/Low to 0/1/2

X = df[features]
y = df[target]

# -------- 5. Split dataset --------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# -------- 6. Train Random Forest Classifier --------
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# -------- 7. Evaluate the model --------
y_pred = model.predict(X_test)
acc = accuracy_score(y_test, y_pred)
print(f"\nModel Accuracy: {acc:.2f}")

cm = confusion_matrix(y_test, y_pred)
print("\nConfusion Matrix:\n", cm)

# -------- 8. Save model and label encoder --------
os.makedirs("models", exist_ok=True)

with open("models/productivity_model.pkl", "wb") as f:
    pickle.dump(model, f)

with open("models/label_encoder.pkl", "wb") as f:
    pickle.dump(le_target, f)

print("\nModel and encoder saved successfully in 'models/' folder.")