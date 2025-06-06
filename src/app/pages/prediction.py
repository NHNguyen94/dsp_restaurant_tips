import pandas as pd
import requests as req
import streamlit as st

response = None
pred_df = pd.DataFrame(
    columns=["Total bill", "Sex", "Smoker", "Day", "Time", "Size", "Predicted tip"]
)

with st.form("form_predict"):
    total_bill = st.text_input("Total bill amount", key="total_bill")
    sex = st.selectbox("Sex", ["Male", "Female"], key="sex")
    smoker = st.selectbox("Are you a smoker ?", ["Yes", "No"], key="smoker")
    day = st.selectbox(
        "What day ?", ["Mon", "Tue", "Wed", "Thur", "Fri", "Sat", "Sun"], key="day"
    )
    time = st.selectbox("And what time ?", ["Lunch", "Dinner"], key="time")
    size = st.text_input("Number of people", key="size")
    uploaded_file = st.file_uploader("Choose a file", ["csv"], key="file")
    submit = st.form_submit_button("Predict")

if submit:
    if uploaded_file:
        csv_file = {"input_file": (uploaded_file.name, uploaded_file, "text/csv")}
        csv_string = uploaded_file.getvalue().decode("utf-8")
        request = req.post(
            "http://127.0.0.1:8000/v1/prediction/predict",
            data=csv_string,
            headers={"Content-Type": "text/csv"},
        )
    else:
        request = req.post(
            "http://127.0.0.1:8000/v1/prediction/predict",
            params={
                "total_bill": total_bill,
                "sex": sex,
                "smoker": smoker,
                "day": day,
                "time": time,
                "size": size,
            },
        )
    response = request.json()

if response:
    for res in response:
        res.pop("predicted_at")
        res.pop("file_path")
        res.pop("prediction_source")
    df = pd.DataFrame(response)
    st.dataframe(df)
