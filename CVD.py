import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
import tkinter as tk
from tkinter import messagebox

# Sample Training Data
X_train = [
    [60, 1, 0, 130, 250, 0, 0, 150, 0, 1, 0, 2, 1],
    [50, 0, 1, 120, 230, 0, 0, 145, 0, 0.8, 1, 1, 2],
    [45, 1, 2, 140, 270, 0, 1, 160, 0, 1.2, 2, 0, 3],
    [70, 0, 1, 150, 290, 1, 2, 140, 1, 0.9, 0, 2, 3],
    [65, 1, 3, 170, 400, 1, 2, 130, 1, 2.5, 2, 3, 3],
    [55, 0, 2, 160, 330, 1, 1, 140, 0, 1.8, 2, 2, 2],
]

y_train = [0, 0, 1, 1, 1, 1]

# Train Standard Scaler & Model
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)

model = RandomForestClassifier(random_state=42)
model.fit(X_train_scaled, y_train)

# Preprocess user input
def preprocess_input(user_data):
    try:
        df = pd.DataFrame([user_data])
        return scaler.transform(df)
    except Exception as e:
        messagebox.showerror("Error", f"Invalid input: {e}")
        return None

# Get user input
def get_user_input():
    try:
        user_data = [
            float(age_entry.get()), int(sex_entry.get()), int(cp_entry.get()),
            float(trestbps_entry.get()), float(chol_entry.get()), int(fbs_entry.get()),
            int(restecg_entry.get()), float(thalach_entry.get()), int(exang_entry.get()),
            float(oldpeak_entry.get()), int(slope_entry.get()), float(ca_entry.get()),
            int(thal_entry.get())
        ]
        return preprocess_input(user_data)
    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numbers in all fields.")
        return None

# Make prediction
def make_prediction(user_input):
    if user_input is None:
        return None
    prediction = model.predict(user_input)[0]
    return "🔴 HIGH RISK: Please consult a doctor!" if prediction == 1 else "🟢 LOW RISK: Keep maintaining a healthy lifestyle!"

# Submit action
def on_submit():
    user_input = get_user_input()
    result = make_prediction(user_input)
    if result:
        root.after(100, lambda: messagebox.showinfo("Prediction Result", result))

# Move to next field on Enter
def on_enter(event, index):
    if index < len(entry_widgets) - 1:
        entry_widgets[index + 1].focus_set()
    else:
        on_submit()  # Submit if last field

# GUI Setup
root = tk.Tk()
root.title("CVD Risk Prediction")
root.configure(bg="#222831")

frame = tk.Frame(root, bg="#30475E", padx=20, pady=20)
frame.pack(padx=20, pady=20)

# Title Label
title_label = tk.Label(frame, text="Cardiovascular Disease Risk Predictor", font=("Times new Roman", 14, "bold"), fg="white", bg="#30475E")
title_label.grid(row=0, column=0, columnspan=2, pady=10)

# Input Fields
entry_bg = "#eeeeee"
label_fg = "white"
entry_widgets = []

fields = [
    ("Age:", "age"), ("Sex (1=Male, 0=Female):", "sex"), ("Chest Pain Type (0-3):", "cp"),
    ("Resting Blood Pressure:", "trestbps"), ("Cholesterol:", "chol"), ("Fasting Blood Sugar (1=Yes, 0=No):", "fbs"),
    ("Resting ECG (0-2):", "restecg"), ("Max Heart Rate:", "thalach"), ("Exercise Induced Angina (1=Yes, 0=No):", "exang"),
    ("ST Depression (0-2.5):", "oldpeak"), ("Slope of ST Segment (0-2):", "slope"),
    ("Major Vessels Colored (0-3):", "ca"), ("Thalassemia (1,2,3):", "thal")
]

for i, (label_text, var_name) in enumerate(fields):
    tk.Label(frame, text=label_text, fg=label_fg, bg="#30475E", font=("Arial", 10, "bold")).grid(row=i + 1, column=0, pady=5, sticky="w")
    entry = tk.Entry(frame, bg=entry_bg, font=("Arial", 10))
    entry.grid(row=i + 1, column=1, pady=5)
    entry.bind("<Return>", lambda event, idx=i: on_enter(event, idx))  # Bind Enter key
    entry_widgets.append(entry)

# Unpack entries
(age_entry, sex_entry, cp_entry, trestbps_entry, chol_entry, fbs_entry, restecg_entry, 
 thalach_entry, exang_entry, oldpeak_entry, slope_entry, ca_entry, thal_entry) = entry_widgets

# Submit Button
submit_button = tk.Button(frame, text="Predict Risk", command=on_submit, font=("Arial", 12, "bold"), fg="white", bg="#F05454", padx=10, pady=5)
submit_button.grid(row=len(fields) + 1, column=0, columnspan=2, pady=20)

root.mainloop()
