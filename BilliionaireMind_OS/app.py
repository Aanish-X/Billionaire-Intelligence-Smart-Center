import streamlit as st
import pandas as pd
import plotly.express as px
import os

# ==============================
# 1. PAGE CONFIG
# ==============================
st.set_page_config(page_title="Billionaire OS", layout="wide")

# ==============================
# 2. PREMIUM DARK THEME
# ==============================
st.markdown("""
<style>
/* Background */
.stApp {
    background: linear-gradient(135deg, #000000, #0f2027);
    color: white;
}

/* Headings */
h1, h2, h3 {
    color: #00FFAA !important;
    text-shadow: 0 0 8px #00FFAA;
}

/* Metric containers */
[data-testid="metric-container"] {
    background: rgba(0,255,170,0.15);
    border: 1px solid #00FFAA;
    padding: 15px;
    border-radius: 12px;
}

/* Metric label */
[data-testid="stMetricLabel"] {
    color: #00FFAA !important;
    font-weight: bold;
    font-size: 16px;
}

/* Metric value */
[data-testid="stMetricValue"] {
    color: white !important;
    font-size: 28px;
    font-weight: bold;
}

/* Text input label */
label {
    color: #00FFAA !important;
    font-weight: bold;
}

/* Text input box */
.stTextInput input {
    background: rgba(0,0,0,0.6);
    color: white;
    border: 2px solid #00FFAA;
}

/* Sidebar text */
section[data-testid="stSidebar"] * {
    color: black !important;
}
</style>
""", unsafe_allow_html=True)

# ==============================
# 3. LOAD DATA
# ==============================
@st.cache_data
def load_data():
    file_path = "data/Billionaires Statistics Dataset.csv"
    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
        df['finalWorth'] = pd.to_numeric(df['finalWorth'], errors='coerce')
        return df
    else:
        st.error("Dataset not found in data folder.")
        st.stop()

df = load_data()

# ==============================
# 4. SIDEBAR FILTERS
# ==============================
st.sidebar.title("⚙️ Control Panel")

country = st.sidebar.multiselect(
    "Select Country",
    options=df['country'].dropna().unique(),
    default=None
)

industry = st.sidebar.multiselect(
    "Select Industry",
    options=df['category'].dropna().unique(),
    default=None
)

filtered_df = df.copy()

if country:
    filtered_df = filtered_df[filtered_df['country'].isin(country)]

if industry:
    filtered_df = filtered_df[filtered_df['category'].isin(industry)]

# ==============================
# 5. TITLE
# ==============================
st.title("🏛 Billionaire Intelligence Command Center")

# ==============================
# 6. KPI METRICS
# ==============================
col1, col2, col3, col4 = st.columns(4)

total_billionaires = len(filtered_df)
total_wealth = filtered_df['finalWorth'].sum()
avg_wealth = filtered_df['finalWorth'].mean()
top_country = filtered_df['country'].mode()[0] if not filtered_df.empty else "N/A"

col1.metric("Total Billionaires", total_billionaires)
col2.metric("Total Wealth ($B)", f"{total_wealth:,.0f}")
col3.metric("Average Wealth ($B)", f"{avg_wealth:,.1f}")
col4.metric("Top Country", top_country)

# ==============================
# 7. TOP 10 RICHEST
# ==============================
st.subheader("🏆 Top 10 Global Titans")

top_10 = filtered_df.sort_values("finalWorth", ascending=False).head(10)

fig = px.bar(
    top_10,
    x="personName",
    y="finalWorth",
    color="finalWorth",
    color_continuous_scale="Tealgrn"
)

fig.update_layout(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font_color="white"
)

st.plotly_chart(fig, use_container_width=True)

# ==============================
# 8. INDUSTRY DOMINANCE
# ==============================
st.subheader("🌌 Industry Wealth Distribution")

industry_chart = px.treemap(
    filtered_df,
    path=['category'],
    values='finalWorth',
    color='finalWorth',
    color_continuous_scale='Tealgrn'
)

industry_chart.update_layout(
    paper_bgcolor="rgba(0,0,0,0)",
    font_color="white"
)

st.plotly_chart(industry_chart, use_container_width=True)

# ==============================
# 9. COUNTRY POWER MAP
# ==============================
st.subheader("🌍 Country Wealth Power")

country_data = (
    filtered_df.groupby("country")["finalWorth"]
    .sum()
    .reset_index()
    .sort_values(by="finalWorth", ascending=False)
    .head(15)
)

fig_country = px.bar(
    country_data,
    x="country",
    y="finalWorth",
    color="finalWorth",
    color_continuous_scale="Tealgrn"
)

fig_country.update_layout(
    paper_bgcolor="rgba(0,0,0,0)",
    font_color="white"
)

st.plotly_chart(fig_country, use_container_width=True)

# ==============================
# 10. DECISION WAR ROOM
# ==============================
st.divider()
st.header("⚡ Strategic Decision War-Room")

problem = st.text_input("Ask a strategic business question:")

if problem:
    st.success("**Elon Musk Approach:** Break it into first principles.")
    st.info("**Jeff Bezos Approach:** Will you regret not doing it at age 80?")
    st.warning("**Warren Buffett Approach:** Only invest if you understand it deeply.")