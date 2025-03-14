import streamlit as st
import pandas as pd
import plotly.express as px

# Load Data
@st.cache_data
def load_data():
    return pd.read_csv("cleaned_reddit_data.csv")

df = load_data()

# Remove unknown values if any exist in 'over_18'
df = df[df["over_18"].notna()]

# Title
st.title("NSFW Content Proportion")

# Calculate NSFW Percentage
nsfw_counts = df["over_18"].value_counts(normalize=True) * 100
nsfw_df = pd.DataFrame({"Category": nsfw_counts.index, "Percentage": nsfw_counts.values})

# Pie Chart
fig = px.pie(nsfw_df, names="Category", values="Percentage", title="NSFW vs SFW Content")
st.plotly_chart(fig)
