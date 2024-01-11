# Description: Dashboard for the credit default predictor

# Libraries
import requests
import streamlit as st
import os

# Processing
import pandas as pd

# Constants
from src.const import default_values

# Working directory check
print(os.getcwd())

# Model server configuration
HOST = os.getenv("MODEL_SERVER_HOST", "http://localhost")
PORT = os.getenv("MODEL_SERVER_PORT", 5000)
ENDPOINT = os.getenv("MODEL_SERVER_ENDPOINT", "/predict")

# Construction of the server url
url = f"{HOST}:{PORT}{ENDPOINT}"

# Headers for the request
headers = {
    "Content-Type": "application/json",
}

# Page configuration
st.set_page_config(page_title="Credit Default Predictor", 
                   page_icon="logo.jpeg", 
                   layout="centered", 
                   initial_sidebar_state="auto", 
                   menu_items=None)

# Addition of title and subtitle
st.title("Credit Default Predictor")
st.markdown("This app predicts the **Default** probability of a credit card user")

# Tabs for manual use and file upload
file_tab, manual_tab  = st.tabs(["File mode", "Manual mode"])

# Structure for manual inputs
with manual_tab:

    # Manual inputs are controlled on the sidebar for better visualization
    with st.sidebar:

        # Logo
        st.image("logo.jpeg", use_column_width=True)

        # Model inputs avaliable on the selectboxes
        device_os = st.selectbox(
            label="Device OS",
            options=['windows', 'other', 'linux', 'macintosh', 'x11'],
            index=2
        )

        employment_status = st.selectbox(
            label="Employment Status",
            options=['CA', 'CB', 'CC', 'CD', 'CE', 'CF', 'CG'],
            index=0
        )

        housing_status = st.selectbox(
            label="Housing Status",
            options=['BA', 'BB', 'BC', 'BD', 'BE', 'BF', 'BG'],
            index=0
        )

        source = st.selectbox(
            label="Source",
            options=['INTERNET', 'TELEAPP'],
            index=0
        )

        payment_type = st.selectbox(
            label="Payment type",
            options=['AA', 'AB', 'AC', 'AD', 'AE'],
            index=0
        )

        # Numerical inputs dealt with manual numeric inputs or + and - buttons
        date_of_birth_distinct_emails_4w = st.number_input(
            label="Date of birth distinct emails 4w",
            value=0,
            min_value=0,
            step=1
        )


        name_email_similarity = st.number_input(label="name_email_similarity", 
                                                min_value=0.0, 
                                                step=0.0001, 
                                                max_value=1.0, 
                                                value=0.0
                                                )
        
        credit_risk_score = st.number_input(label="credit_risk_score", 
                                            min_value=-1000, 
                                            step=1, 
                                            max_value=1000, 
                                            value=1
                                            )
        
        customer_age = st.number_input(label="customer_age", 
                                       min_value=1, 
                                       step=1, 
                                       max_value=100, 
                                       value=18
                                       )
        
        month = st.number_input(label="month", 
                                min_value=0, 
                                step=1, 
                                max_value=7, 
                                value=1
                                )
        
        has_other_cards = st.number_input(label="has_other_cards", 
                                          min_value=0, 
                                          step=1, 
                                          max_value=1, 
                                          value=0
                                          )
        
        proposed_credit_limit = st.number_input(label="proposed_credit_limit", 
                                                min_value=0, 
                                                step=1, 
                                                max_value=1000000, 
                                                value=1
                                                )
        
        prev_address_months_count = st.number_input(label="prev_address_months_count", 
                                                    min_value=0, 
                                                    step=1, 
                                                    max_value=1000, 
                                                    value=0
                                                    )
        
        zip_count_4w = st.number_input(label="zip_count_4w", 
                                       min_value=1, 
                                       step=1, 
                                       max_value=10000, 
                                       value=1
                                       )
        
        income = st.number_input(label="income", 
                                 min_value=0.0, 
                                 step=0.1, 
                                 max_value=1.0, 
                                 value=0.1
                                 )
        
        device_distinct_emails_8w = st.number_input(label="device_distinct_emails_8w", 
                                                    min_value=0, 
                                                    step=1, 
                                                    max_value=10, 
                                                    value=0
                                                    )
        
        bank_months_count = st.number_input(label="bank_months_count", 
                                            min_value=0, 
                                            step=1, 
                                            max_value=1200, 
                                            value=0
                                            )
        
        # Binary variables dealt with selectboxes
        phone_home_valid = st.selectbox(label="phone_home_valid", 
                                        options=["Yes", "No"], 
                                        index=0
                                        )

        foreign_request = st.selectbox(label="foreign_request", 
                                       options=["Yes", "No"], 
                                       index=0
                                       )

        keep_alive_session = st.selectbox(label="keep_alive_session", 
                                          options=["Yes", "No"], 
                                          index=0
                                          )

        email_is_free = st.selectbox(label="email_is_free", 
                                     options=["Yes", "No"], 
                                     index=0
                                     )
        
        # Parse options to boolean for the model
        phone_home_valid = phone_home_valid == "Yes"
        foreign_request = foreign_request == "Yes"
        keep_alive_session = keep_alive_session == "Yes"
        email_is_free = email_is_free == "Yes"

    # Summary of manual imputs for the user
    selected_values = {}

    for variable_name, default_value in default_values.items():
        selected_values[variable_name] = st.sidebar.number_input(
            label=variable_name.capitalize(),
            value=default_value
        )
    selected_values['Variable1'] = st.sidebar.number_input("Variable 1", value=0.0)
    selected_values['Variable2'] = st.sidebar.text_input("Variable 2", value='')

    st.markdown("### Summary of inputs")
    summary = pd.DataFrame({'Variable': list(selected_values.keys()), 'Valor': list(selected_values.values())})
    st.table(summary)

# Configuration for file upload mode
with file_tab:
    csv = st.file_uploader(
        label="Upload a CSV or excel file",
        type=["csv", "xlsx", "xls"]
    )

# Only request server if data changes to avoid unnecessary requests
@st.cache_data
def post(json: dict) -> requests.Response:
    
    # Post data to model server
    return requests.post(
        url=url,
        headers=headers,
        json=json
    )

# Structure for csv and excel files
if csv:

    try:
        uploaded_data_df = pd.read_csv(csv)
    except UnicodeDecodeError:
        uploaded_data_df = pd.read_excel(csv)
    
    with file_tab:
        st.dataframe(uploaded_data_df)

    # Convert to json for the request
    data = uploaded_data_df.to_dict(orient="records")
    response = post(json={"data": data})

# Structure for manual inputs
else:

    # Build the json from the manual inputs on frontend
    data = [{
            "device_os": device_os,
            "source": source,
            "housing_status": housing_status,
            "employment_status": employment_status,
            "payment_type": payment_type,
            "date_of_birth_distinct_emails_4w": date_of_birth_distinct_emails_4w,
            "name_email_similarity": name_email_similarity,
            "credit_risk_score": credit_risk_score,
            "customer_age": customer_age,
            "month": month,
            "has_other_cards": has_other_cards,
            "proposed_credit_limit": proposed_credit_limit,
            "prev_address_months_count": prev_address_months_count,
            "zip_count_4w": zip_count_4w,
            "income": income,
            "device_distinct_emails_8w": device_distinct_emails_8w,
            "bank_months_count": bank_months_count,
            "phone_home_valid": phone_home_valid,
            "foreign_request": foreign_request,
            "keep_alive_session": keep_alive_session,
            "email_is_free": email_is_free
        }]

    # Respond to the post request with the predictions
    response = post(json={"data": data})

# 
st.markdown("### Predicted probability")
probabilities = pd.DataFrame(response.json()["probability"])
st.table(probabilities)

# Threshold for fraud
threshold = st.number_input(
    "Threshold",
    min_value=0.0,
    max_value=1.0,
    step=0.05,
    value=0.0
)

defaults = ["Potential fraud" if p > threshold else "Normal" for p in response.json()["probability"]]

st.markdown("### Results")
st.table(defaults)