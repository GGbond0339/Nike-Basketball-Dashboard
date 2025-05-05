
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
product_lines = st.sidebar.multiselect("Product Line", df["ProductLine"].unique(), default=df["ProductLine"].unique())
regions = st.sidebar.multiselect("Region", df["Region"].unique(), default=df["Region"].unique())

# Filtered Data
filtered_df = df[
    (df["Date"] >= pd.to_datetime(date_range[0])) &
    (df["Date"] <= pd.to_datetime(date_range[1])) &
    (df["ProductLine"].isin(product_lines)) &
    (df["Region"].isin(regions))
]

# Header
st.markdown("## 🏀 Nike Basketball Sales Performance Dashboard (2024 H1)")
st.markdown("Analyze Nike's basketball shoe performance across regions, products, and time.")

# KPIs
total_sales = filtered_df["Sales"].sum()
avg_rating = filtered_df["CustomerRating"].mean()
best_region = filtered_df.groupby("Region")["Sales"].sum().idxmax()
best_product = filtered_df.groupby("ProductLine")["Sales"].sum().idxmax()

col1, col2, col3, col4 = st.columns(4)
col1.metric("💰 Total Sales", f"${total_sales:,.0f}")
col2.metric("⭐ Avg Rating", f"{avg_rating:.2f}")
col3.metric("📍Top Region", best_region)
col4.metric("👟 Top Product Line", best_product)

# Visualization 1: Sales Over Time
st.subheader("📈 Sales Trend Over Time")
fig1 = px.line(filtered_df.groupby("Date")["Sales"].sum().reset_index(), x="Date", y="Sales", title="Total Sales Over Time")
st.plotly_chart(fig1, use_container_width=True)

# Visualization 2: Sales by Product Line
st.subheader("🧱 Product Line Sales Distribution")
fig2 = px.bar(filtered_df.groupby("ProductLine")["Sales"].sum().reset_index(), x="ProductLine", y="Sales", title="Sales by Product Line", text_auto=True)
st.plotly_chart(fig2, use_container_width=True)

# Visualization 3: Customer Rating Histogram
st.subheader("⭐ Customer Rating Distribution")
fig3 = px.histogram(filtered_df, x="CustomerRating", nbins=10, title="Customer Rating Distribution")
st.plotly_chart(fig3, use_container_width=True)

# Optional Geo Chart if location is available
if "Latitude" in df.columns and "Longitude" in df.columns:
    st.subheader("🗺️ Geographic Sales Map")
    geo_df = filtered_df.groupby(["Region", "Latitude", "Longitude"])["Sales"].sum().reset_index()
    fig4 = px.scatter_geo(geo_df, lat="Latitude", lon="Longitude", size="Sales", color="Region",
                          projection="natural earth", title="Sales by Region")
    st.plotly_chart(fig4, use_container_width=True)

# Download button
st.download_button("⬇️ Download Filtered Data", data=filtered_df.to_csv(index=False), file_name="filtered_nike_basketball_sales.csv")
