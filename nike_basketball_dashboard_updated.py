
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Nike Basketball Dashboard", layout="wide")

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("nike_basketball_sales_v2.csv")
    df["Date"] = pd.to_datetime(df["Date"])
    return df

df = load_data()

# Sidebar - Filters
st.sidebar.title("🔧 Filters")
date_range = st.sidebar.date_input("Select Date Range", [df["Date"].min(), df["Date"].max()])
series = st.sidebar.multiselect("Shoe Series", df["Series"].unique(), default=df["Series"].unique())
stores = st.sidebar.multiselect("Store (Region)", df["Store"].unique(), default=df["Store"].unique())

# Filtered Data
filtered_df = df[
    (df["Date"] >= pd.to_datetime(date_range[0])) &
    (df["Date"] <= pd.to_datetime(date_range[1])) &
    (df["Series"].isin(series)) &
    (df["Store"].isin(stores))
]

# Header
st.markdown("## 🏀 Nike Basketball Shoe Sales Dashboard (2024 H1)")
st.markdown("Analyze Nike's basketball shoe sales performance by city and shoe line.")

# KPIs
total_sales = filtered_df["SalesAmount"].sum()
total_units = filtered_df["UnitsSold"].sum()
best_store = filtered_df.groupby("Store")["SalesAmount"].sum().idxmax()
best_series = filtered_df.groupby("Series")["SalesAmount"].sum().idxmax()

col1, col2, col3, col4 = st.columns(4)
col1.metric("💰 Total Sales", f"${total_sales:,.0f}")
col2.metric("📦 Units Sold", f"{total_units:,}")
col3.metric("🏪 Top Store", best_store)
col4.metric("👟 Top Series", best_series)

# Visualization 1: Sales Trend Over Time
st.subheader("📈 Sales Trend Over Time")
fig1 = px.line(filtered_df.groupby("Date")["SalesAmount"].sum().reset_index(),
               x="Date", y="SalesAmount", title="Total Sales Over Time")
st.plotly_chart(fig1, use_container_width=True)

# Visualization 2: Series Sales Distribution
st.subheader("🧱 Sales by Shoe Series")
fig2 = px.bar(filtered_df.groupby("Series")["SalesAmount"].sum().reset_index(),
              x="Series", y="SalesAmount", title="Total Sales by Shoe Series", text_auto=True)
st.plotly_chart(fig2, use_container_width=True)

# Visualization 3: Store Comparison
st.subheader("🏙️ Sales by Store")
fig3 = px.bar(filtered_df.groupby("Store")["SalesAmount"].sum().reset_index(),
              x="Store", y="SalesAmount", title="Total Sales by Store", text_auto=True)
st.plotly_chart(fig3, use_container_width=True)

# Download button
st.download_button("⬇️ Download Filtered Data", data=filtered_df.to_csv(index=False), file_name="filtered_nike_basketball_sales.csv")
