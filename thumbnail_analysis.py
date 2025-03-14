import streamlit as st
import pandas as pd
import plotly.express as px

# 1) Common Thumbnail Aspect Ratios
# Bar Chart for the same
# Load Data
@st.cache_data
def load_data():
    return pd.read_csv("cleaned_reddit_data.csv")

df = load_data()

# Aspect Ratio Calculation
df["aspect_ratio"] = df["thumbnail_width"] / df["thumbnail_height"]

# Plot Histogram
fig = px.histogram(df, x="aspect_ratio", title="📏 Distribution of Thumbnail Aspect Ratios", nbins=20)
st.plotly_chart(fig) 



# 2) Most Common Thumbnail Sizes

size_counts = df.groupby(["thumbnail_width", "thumbnail_height"]).size().reset_index(name="count")

fig = px.bar(size_counts.sort_values("count", ascending=False).head(10),
             x="thumbnail_width", y="count", color="thumbnail_height",
             title="🔝 Top 10 Most Common Thumbnail Sizes",
             labels={"thumbnail_width": "Width", "count": "Frequency"})
st.plotly_chart(fig)


# 3) Post Size by Flair
df["thumbnail_area"] = df["thumbnail_width"] * df["thumbnail_height"]
flair_avg_size = df.groupby("link_flair_text")["thumbnail_area"].mean().reset_index()

fig = px.bar(flair_avg_size.sort_values("thumbnail_area", ascending=False),
             x="link_flair_text", y="thumbnail_area",
             title="📊 Average Thumbnail Size by Flair",
             labels={"link_flair_text": "Flair", "thumbnail_area": "Avg. Size"})
st.plotly_chart(fig)


# Do Premium Users Upload Larger Thumbnails?

fig = px.box(df, x="author_premium", y="thumbnail_area",
             title="📊 Thumbnail Area Distribution (Premium vs. Non-Premium Users)",
             labels={"author_premium": "Premium User", "thumbnail_area": "Thumbnail Area"})
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! THIRD GRAPH  !!!!!!!!!!!!!!!
# st.plotly_chart(fig)








