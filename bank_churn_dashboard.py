import streamlit as st
import pandas as pd
import plotly.express as px

# ----------------------
# Login Page
# ----------------------
def login():
    st.title("🔐 Customer Dashboard Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username == "admin" and password == "1234":
            st.session_state["authenticated"] = True
        else:
            st.error("Invalid credentials")

if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    login()
    st.stop()

# ----------------------
# Load Data
# ----------------------
df = pd.read_csv("cleaned_file.csv")  # Replace with your actual path

# ----------------------
# Sidebar Filters
# ----------------------
st.sidebar.header("🔍 Filter Customer Data")
gender = st.sidebar.multiselect("Gender", options=df["gender"].unique())
region = st.sidebar.multiselect("Region Category", options=df["region_category"].unique())
membership = st.sidebar.multiselect("Membership Category", options=df["membership_category"].unique())
medium = st.sidebar.multiselect("Medium of Operation", options=df["medium_of_operation"].unique())
internet = st.sidebar.multiselect("Internet Option", options=df["internet_option"].unique())
complaint_status = st.sidebar.multiselect("Complaint Status", options=df["complaint_status"].unique())
feedback = st.sidebar.multiselect("Feedback", options=df["feedback"].unique())

# Apply Filters
filtered_df = df.copy()
if gender:
    filtered_df = filtered_df[filtered_df["gender"].isin(gender)]
if region:
    filtered_df = filtered_df[filtered_df["region_category"].isin(region)]
if membership:
    filtered_df = filtered_df[filtered_df["membership_category"].isin(membership)]
if medium:
    filtered_df = filtered_df[filtered_df["medium_of_operation"].isin(medium)]
if internet:
    filtered_df = filtered_df[filtered_df["internet_option"].isin(internet)]
if complaint_status:
    filtered_df = filtered_df[filtered_df["complaint_status"].isin(complaint_status)]
if feedback:
    filtered_df = filtered_df[filtered_df["feedback"].isin(feedback)]

# ----------------------
# Dashboard Title
# ----------------------
st.title("📊 Bank Customer Churn Dashboard")

# Churn Risk Pie Chart
fig1 = px.pie(filtered_df, names='churn_risk_score', title='Churn Risk Distribution')
st.plotly_chart(fig1)

# Gender vs Churn Risk
fig2 = px.histogram(filtered_df, x='gender', color='churn_risk_score', barmode='group',
                    title='Churn Risk by Gender')
st.plotly_chart(fig2)

# Membership Category vs Avg Transaction Value
fig3 = px.box(filtered_df, x='membership_category', y='avg_transaction_value', color='membership_category',
              title='Transaction Value by Membership Category')
st.plotly_chart(fig3)

# Internet Option Usage
internet_df = filtered_df.groupby('internet_option')['churn_risk_score'].count().reset_index()
fig4 = px.bar(internet_df, x='internet_option', y='churn_risk_score', title='Internet Option vs Churn Count')
st.plotly_chart(fig4)

# Login Frequency vs Time Spent
fig5 = px.scatter(filtered_df, x='avg_frequency_login_days', y='avg_time_spent',
                  color='churn_risk_score', size='avg_transaction_value',
                  title='Login Frequency vs Time Spent')
st.plotly_chart(fig5)

# Feedback vs Churn Risk
fig6 = px.histogram(filtered_df, x='feedback', color='churn_risk_score', barmode='group',
                    title='Feedback Distribution by Churn Risk')
st.plotly_chart(fig6)

# Complaints Impact
fig7 = px.histogram(filtered_df, x='complaint_status', color='churn_risk_score',
                    title='Complaints vs Churn Risk')
st.plotly_chart(fig7)

# ----------------------
# Raw Data Table
# ----------------------
st.subheader("🧾 Filtered Data Table")
st.dataframe(filtered_df, use_container_width=True)

# ----------------------
# End
# ----------------------
