import streamlit as st
import pandas as pd
import numpy as np
import pickle
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Load model & encoders
@st.cache_resource
def load_model():
    with open('models/model.pkl', 'rb') as f:
        model = pickle.load(f)
    with open('models/le_category.pkl', 'rb') as f:
        le_category = pickle.load(f)
    with open('models/le_region.pkl', 'rb') as f:
        le_region = pickle.load(f)
    return model, le_category, le_region

@st.cache_data
def load_data():
    return pd.read_csv('data/sales_data.csv')

# Page config
st.set_page_config(
    page_title="Sales Forecasting Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Sales Forecasting Dashboard")
st.markdown("---")

# Load everything
model, le_category, le_region = load_model()
df = load_data()
df['date'] = pd.to_datetime(df['date'])

# ---- Sidebar Filters ----
st.sidebar.header("🔍 Filters")
selected_region = st.sidebar.multiselect(
    "Region", df['region'].unique(), default=df['region'].unique()
)
selected_category = st.sidebar.multiselect(
    "Category", df['category'].unique(), default=df['category'].unique()
)

filtered_df = df[
    (df['region'].isin(selected_region)) & 
    (df['category'].isin(selected_category))
]

# ---- KPIs ----
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Revenue", f"${filtered_df['revenue'].sum():,.0f}")
col2.metric("Total Orders", f"{len(filtered_df):,}")
col3.metric("Avg Order Value", f"${filtered_df['revenue'].mean():,.0f}")
col4.metric("Avg Discount", f"{filtered_df['discount'].mean()*100:.1f}%")

st.markdown("---")

# ---- Charts ----
col1, col2 = st.columns(2)

with col1:
    st.subheader("Revenue by Category")
    cat_revenue = filtered_df.groupby('category')['revenue'].sum().reset_index()
    fig = px.pie(cat_revenue, values='revenue', names='category')
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Revenue by Region")
    reg_revenue = filtered_df.groupby('region')['revenue'].sum().reset_index()
    fig = px.bar(reg_revenue, x='region', y='revenue', color='region')
    st.plotly_chart(fig, use_container_width=True)

# Revenue over time
st.subheader("Revenue Over Time")
time_revenue = filtered_df.groupby('date')['revenue'].sum().reset_index()
fig = px.line(time_revenue, x='date', y='revenue')
st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# ---- ML Prediction ----
st.subheader("🤖 Predict Revenue")

col1, col2, col3 = st.columns(3)
with col1:
    category = st.selectbox("Category", le_category.classes_)
    quantity = st.number_input("Quantity", 1, 100, 10)
with col2:
    region = st.selectbox("Region", le_region.classes_)
    price = st.number_input("Price ($)", 10, 1000, 100)
with col3:
    month = st.selectbox("Month", range(1, 13))
    discount = st.slider("Discount", 0.0, 0.5, 0.1)

if st.button("🔮 Predict", type="primary"):
    input_data = pd.DataFrame([{
        'month': month,
        'day_of_week': datetime.now().weekday(),
        'quarter': (month - 1) // 3 + 1,
        'quantity': quantity,
        'price': price,
        'discount': discount,
        'category_encoded': le_category.transform([category])[0],
        'region_encoded': le_region.transform([region])[0]
    }])
    
    prediction = model.predict(input_data)[0]
    st.success(f"💰 Predicted Revenue: **${prediction:,.2f}**")