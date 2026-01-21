import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------
# Page configuration
# -----------------------------
st.set_page_config(
    page_title="Video Game Sales Dashboard",
    layout="wide"
)

st.title("🎮 Video Game Sales Interactive Dashboard")

# -----------------------------
# Load data
# -----------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("vgsales.csv")
    df = df.dropna(subset=["Year"])
    df["Year"] = df["Year"].astype(int)
    return df

df = load_data()

# -----------------------------
# Sidebar filters
# -----------------------------
st.sidebar.header("🔎 Filters")

selected_genres = st.sidebar.multiselect(
    "Select Genre",
    options=sorted(df["Genre"].unique()),
    default=sorted(df["Genre"].unique())
)

selected_platforms = st.sidebar.multiselect(
    "Select Platform",
    options=sorted(df["Platform"].unique()),
    default=sorted(df["Platform"].unique())
)

year_min, year_max = int(df["Year"].min()), int(df["Year"].max())
selected_years = st.sidebar.slider(
    "Select Year Range",
    min_value=year_min,
    max_value=year_max,
    value=(2000, year_max)
)

# -----------------------------
# Apply filters (LINKED VIEWS)
# -----------------------------
filtered_df = df[
    (df["Genre"].isin(selected_genres)) &
    (df["Platform"].isin(selected_platforms)) &
    (df["Year"].between(selected_years[0], selected_years[1]))
]

# -----------------------------
# Layout
# -----------------------------
col1, col2 = st.columns(2)

# -----------------------------
# Visualization 1: Global Sales by Genre
# -----------------------------
genre_sales = (
    filtered_df
    .groupby("Genre", as_index=False)["Global_Sales"]
    .sum()
    .sort_values("Global_Sales", ascending=False)
)

fig1 = px.bar(
    genre_sales,
    x="Genre",
    y="Global_Sales",
    title="Global Sales by Genre",
    labels={"Global_Sales": "Sales (millions)"}
)

col1.plotly_chart(fig1, use_container_width=True)

# -----------------------------
# Visualization 2: Global Sales by Platform
# -----------------------------
platform_sales = (
    filtered_df
    .groupby("Platform", as_index=False)["Global_Sales"]
    .sum()
    .sort_values("Global_Sales", ascending=False)
)

fig2 = px.bar(
    platform_sales,
    x="Platform",
    y="Global_Sales",
    title="Global Sales by Platform",
    labels={"Global_Sales": "Sales (millions)"}
)

col2.plotly_chart(fig2, use_container_width=True)

# -----------------------------
# Visualization 3: Regional Sales Distribution
# -----------------------------
region_sales = pd.DataFrame({
    "Region": ["North America", "Europe", "Japan", "Other"],
    "Sales": [
        filtered_df["NA_Sales"].sum(),
        filtered_df["EU_Sales"].sum(),
        filtered_df["JP_Sales"].sum(),
        filtered_df["Other_Sales"].sum()
    ]
})

fig3 = px.bar(
    region_sales,
    x="Region",
    y="Sales",
    title="Regional Sales Distribution",
    labels={"Sales": "Sales (millions)"}
)

col1.plotly_chart(fig3, use_container_width=True)

# -----------------------------
# Visualization 4: Global Sales Over Time
# -----------------------------
yearly_sales = (
    filtered_df
    .groupby("Year", as_index=False)["Global_Sales"]
    .sum()
)

fig4 = px.line(
    yearly_sales,
    x="Year",
    y="Global_Sales",
    title="Global Sales Over Time",
    labels={"Global_Sales": "Sales (millions)"}
)

col2.plotly_chart(fig4, use_container_width=True)

# -----------------------------
# Footer
# -----------------------------
st.markdown(
    """
    **Dashboard Summary:**  
    This interactive dashboard allows users to explore video game sales
    by genre, platform, region, and time. Filters enable linked exploration
    across all views.
    """
)

