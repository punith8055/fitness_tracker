import streamlit as st
import numpy as np
import pandas as pd
import time
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import matplotlib.pyplot as plt
import seaborn as sns
import base64
import warnings
warnings.filterwarnings('ignore')

# ---------------------------
# 🛑 USER AUTHENTICATION
# ---------------------------
USER_CREDENTIALS = {"admin": "password123", "user1": "fitness2025"}

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# ---------------------------
# 🔐 LOGIN PAGE
# ---------------------------
def login_page():
    st.markdown("## 🔒 Login to Access Fitness Tracker")
    username = st.text_input("👤 Username", key="username")
    password = st.text_input("🔑 Password", type="password", key="password")

    if st.button("Login"):
        if username in USER_CREDENTIALS and USER_CREDENTIALS[username] == password:
            st.success(f"🎉 Welcome, {username}!")
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("❌ Invalid username or password. Please try again!")

# ---------------------------
# 🚪 LOGOUT FUNCTION
# ---------------------------
def logout():
    st.session_state.logged_in = False
    st.rerun()

# ---------------------------
# 🏋️ MAIN FITNESS TRACKER PAGE
# ---------------------------
def fitness_tracker():
    st.sidebar.button("Logout", on_click=logout)

    st.write("## 🎯 Personal Fitness Tracker")
    st.write("Pass your parameters such as `Age`, `Gender`, `BMI`, etc., and predict kilocalories burned!")

    st.sidebar.header("⚙️ User Input Parameters")

    def user_input_features():
        age = st.sidebar.slider("Age: ", 10, 100, 30)
        bmi = st.sidebar.slider("BMI: ", 15, 40, 20)
        duration = st.sidebar.slider("Duration (min): ", 0, 35, 15)
        heart_rate = st.sidebar.slider("Heart Rate: ", 60, 130, 80)
        body_temp = st.sidebar.slider("Body Temperature (C): ", 36, 42, 38)
        gender_button = st.sidebar.radio("Gender: ", ("Male", "Female"))
        gender = 1 if gender_button == "Male" else 0

        data_model = {
            "Age": age,
            "BMI": bmi,
            "Duration": duration,
            "Heart_Rate": heart_rate,
            "Body_Temp": body_temp,
            "Gender_male": gender
        }
        return pd.DataFrame(data_model, index=[0])

    df = user_input_features()

    with st.spinner("🔍 Analyzing your parameters..."):
        time.sleep(1)
    st.success("✅ Parameters successfully recorded!")
    st.write(df)

    # Load data
    calories = pd.read_csv("calories.csv")
    exercise = pd.read_csv("exercise.csv")

    exercise_df = exercise.merge(calories, on="User_ID")
    exercise_df.drop(columns="User_ID", inplace=True)

    # Split data
    exercise_train_data, exercise_test_data = train_test_split(exercise_df, test_size=0.2, random_state=1)

    # Add BMI column
    for data in [exercise_train_data, exercise_test_data]:
        data["BMI"] = data["Weight"] / ((data["Height"] / 100) ** 2)
        data["BMI"] = round(data["BMI"], 2)

    exercise_train_data = exercise_train_data[["Gender", "Age", "BMI", "Duration", "Heart_Rate", "Body_Temp", "Calories"]]
    exercise_test_data = exercise_test_data[["Gender", "Age", "BMI", "Duration", "Heart_Rate", "Body_Temp", "Calories"]]
    exercise_train_data = pd.get_dummies(exercise_train_data, drop_first=True)
    exercise_test_data = pd.get_dummies(exercise_test_data, drop_first=True)

    X_train = exercise_train_data.drop("Calories", axis=1)
    y_train = exercise_train_data["Calories"]
    X_test = exercise_test_data.drop("Calories", axis=1)
    y_test = exercise_test_data["Calories"]

    with st.spinner("🤖 Training model..."):
        random_reg = RandomForestRegressor(n_estimators=1000, max_features=3, max_depth=6)
        random_reg.fit(X_train, y_train)
    st.success("🎉 Model trained successfully!")

    df = df.reindex(columns=X_train.columns, fill_value=0)

    with st.spinner("⚡ Calculating calories burned..."):
        prediction = random_reg.predict(df)
        time.sleep(1)
    st.success(f"🔥 Predicted: **{round(prediction[0], 2)} kilocalories**")

    st.write("---")
    with st.expander("🔍 Show Similar Results"):
        calorie_range = [prediction[0] - 10, prediction[0] + 10]
        similar_data = exercise_df[(exercise_df["Calories"] >= calorie_range[0]) & (exercise_df["Calories"] <= calorie_range[1])]
        st.write(similar_data.sample(5))

    st.write("---")
    st.header("📊 General Information:")

    boolean_age = (exercise_df["Age"] < df["Age"].values[0]).tolist()
    boolean_duration = (exercise_df["Duration"] < df["Duration"].values[0]).tolist()
    boolean_body_temp = (exercise_df["Body_Temp"] < df["Body_Temp"].values[0]).tolist()
    boolean_heart_rate = (exercise_df["Heart_Rate"] < df["Heart_Rate"].values[0]).tolist()

    st.write("👴 You are older than")
    st.progress(round(sum(boolean_age) / len(boolean_age), 2))

    st.write("🏃 Your exercise duration is higher than")
    st.progress(round(sum(boolean_duration) / len(boolean_duration), 2))

    st.write("💓 You have a higher heart rate than")
    st.progress(round(sum(boolean_heart_rate) / len(boolean_heart_rate), 2))

    st.write("🌡️ You have a higher body temperature than")
    st.progress(round(sum(boolean_body_temp) / len(boolean_body_temp), 2))

    # ---------------------------
    # 📺 Live Fitness Classes/Tutorials Section
    # ---------------------------
    st.write("---")
    st.write("## 📺 Live Fitness Classes/Tutorials")
    st.write("Join live workout classes or view helpful fitness tutorials on YouTube!")

    st.write("### 🎥 Recommended Fitness Class")
    st.markdown("""
        <iframe width="560" height="315" src="https://www.youtube.com/embed/6yfkX6Rf0mQ" 
        title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
        """, unsafe_allow_html=True)

    st.write("### 🧘 More Workout Tutorials:")
    st.markdown("""
    1. [Morning Stretch Routine](https://www.youtube.com/watch?v=itJE4neqDJw)
    2. [High-Intensity Interval Training (HIIT)](https://www.youtube.com/watch?v=hOHhelsCHu4)
    3. [Yoga for Flexibility](https://www.youtube.com/watch?v=U-oPOj0W9Sc)
    """)

# ---------------------------
# 🚀 MAIN LOGIC TO SWITCH PAGES
# ---------------------------
if not st.session_state.logged_in:
    login_page()
else:
    fitness_tracker()
