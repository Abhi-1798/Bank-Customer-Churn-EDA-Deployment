import streamlit as st
import pandas as pd
import plotly.express as px

# ----------------------
# Login Page
# ----------------------
def login():
    st.title("\U0001F512 Customer Dashboard Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username == "abhishek" and password == "1234567":
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
df = pd.read_csv("cleaned_file.csv")
df['churn_risk_score'] = df['churn_risk_score'].astype(str)

# ----------------------
# Sidebar Filters
# ----------------------
st.sidebar.header("\U0001F50D Filter Customer Data")
gender = st.sidebar.multiselect("Gender", options=df["gender"].dropna().unique())
region = st.sidebar.multiselect("Region Category", options=df["region_category"].dropna().unique())
membership = st.sidebar.multiselect("Membership Category", options=df["membership_category"].dropna().unique())
medium = st.sidebar.multiselect("Medium of Operation", options=df["medium_of_operation"].dropna().unique())
internet = st.sidebar.multiselect("Internet Option", options=df["internet_option"].dropna().unique())
complaint_status = st.sidebar.multiselect("Complaint Status", options=df["complaint_status"].dropna().unique())
feedback = st.sidebar.multiselect("Feedback", options=df["feedback"].dropna().unique())

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
st.title("\U0001F4CA Bank Customer Churn Dashboard")

# ----------------------
# Metrics
# ----------------------
col1, col2, col3, col4 = st.columns(4)
col1.metric("\U0001F465 Total Customers", len(filtered_df))
col2.metric("\U0001F4B0 Avg Points in Wallet", round(filtered_df['points_in_wallet'].mean(), 2))
col3.metric("\U0001F4B3 Avg Transaction Value", round(filtered_df['avg_transaction_value'].mean(), 2))
col4.metric("\u23F1 Avg Time Spent", round(filtered_df['avg_time_spent'].mean(), 2))

# ----------------------
# Visualizations
# ----------------------

# Churn Risk Pie Chart
if not filtered_df['churn_risk_score'].isnull().all():
    fig1 = px.pie(filtered_df, names='churn_risk_score', title='Churn Risk Distribution')
    st.plotly_chart(fig1)
    st.markdown("**🔹 This pie chart shows the proportion of customers in each churn risk category. It helps identify how many are likely to churn vs. stay.**")

# Gender vs Churn Risk
if not filtered_df['gender'].isnull().all():
    fig2 = px.histogram(filtered_df, x='gender', color='churn_risk_score', barmode='group',
                        title='Churn Risk by Gender')
    st.plotly_chart(fig2)
    st.markdown("**🔹 Understand how churn risk varies across gender. Useful for targeting gender-specific retention efforts.**")

# Membership Category vs Avg Transaction Value
if not filtered_df['membership_category'].isnull().all():
    fig3 = px.box(filtered_df, x='membership_category', y='avg_transaction_value', color='membership_category',
                  title='Transaction Value by Membership Category')
    st.plotly_chart(fig3)
    st.markdown("**🔹 See spending behavior segmented by membership tiers. Useful to know which tier brings high value.**")

# Internet Option Usage
if 'internet_option' in filtered_df.columns and not filtered_df['internet_option'].isnull().all():
    internet_df = filtered_df.groupby('internet_option')['churn_risk_score'].count().reset_index()
    fig4 = px.bar(internet_df, x='internet_option', y='churn_risk_score', title='Internet Option vs Churn Count')
    st.plotly_chart(fig4)
    st.markdown("**🔹 Highlights preferred internet access methods and their association with churn.**")

# Login Frequency vs Time Spent
if not filtered_df['avg_frequency_login_days'].isnull().all():
    fig5 = px.scatter(filtered_df, x='avg_frequency_login_days', y='avg_time_spent',
                      color='churn_risk_score', size='avg_transaction_value',
                      title='Login Frequency vs Time Spent')
    st.plotly_chart(fig5)
    st.markdown("**🔹 Shows engagement patterns: more logins & time spent often correlates with lower churn.**")

# Feedback vs Churn Risk
if not filtered_df['feedback'].isnull().all():
    fig6 = px.histogram(filtered_df, x='feedback', color='churn_risk_score', barmode='group',
                        title='Feedback Distribution by Churn Risk')
    st.plotly_chart(fig6)
    st.markdown("**🔹 Helps identify what kind of feedback is associated with higher churn risk.**")

# Complaints Impact
if not filtered_df['complaint_status'].isnull().all():
    fig7 = px.histogram(filtered_df, x='complaint_status', color='churn_risk_score',
                        title='Complaints vs Churn Risk')
    st.plotly_chart(fig7)
    st.markdown("**🔹 Displays how unresolved complaints or types of resolution affect churn.**")

# ----------------------
# Dynamic Category-Based Table or Chart
# ----------------------
st.subheader("\U0001F4C8 Dynamic Summary by Category")

category = st.selectbox("Select Category", ["gender", "region_category", "membership_category", "churn_risk_score"])
view_type = st.radio("Choose View Type", ["Table", "Bar Chart"])

summary_df = (
    filtered_df.groupby(category)
    .agg(Customer_Count=('customer_id', 'count'))
    .reset_index()
)

if view_type == "Table":
    st.dataframe(summary_df, use_container_width=True)
else:
    fig = px.bar(summary_df, x=category, y='Customer_Count', title=f"Customer Count by {category.title()}")
    st.plotly_chart(fig, use_container_width=True)

# ----------------------
# End
# ----------------------
