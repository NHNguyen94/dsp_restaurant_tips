import streamlit as st
import requests as req
import pandas as pd

response = None
pred_df = pd.DataFrame(
    columns=["Total bill", "Sex", "Smoker", "Day", "Time", "Size", "Predicted tip", "Predicted at",
    "Prediction source", "File Path"]
)

with st.form("form_predict"):
    start_date = st.date_input("Predictions from...", value=None, key="date_start")
    end_date = st.date_input("to...", value=None, key="date_end")
    pred_source = st.selectbox(
        "Prediction type", ["Webapp", "Scheduled", "All"], key="pred_source"
    )
    submit = st.form_submit_button("Get your predictions")

if submit:
    if pred_source == "Scheduled":
        pred_source = "scheduled_predictions"
    request = req.post(
        "http://127.0.0.1:8000/v1/prediction/past-predictions",
        params={
            "start_date": start_date,
            "end_date": end_date,
            "prediction_source": pred_source.lower(),
        },
    )
    response = request.json()
    print(response)

if response:
    st.dataframe(response)
