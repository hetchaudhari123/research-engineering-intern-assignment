import streamlit as st
import pandas as pd
import plotly.express as px

# Load Data
@st.cache_data
def load_data():
    return pd.read_csv("cleaned_reddit_data.csv")

df = load_data()

# Categorize posts as containing external links or not
df["has_external_link"] = df["url_overridden_by_dest"].notna()

# Count the occurrences
external_link_counts = df["has_external_link"].value_counts().reset_index()
external_link_counts.columns = ["Has External Link", "Count"]

# Convert boolean values to labels
external_link_counts["Has External Link"] = external_link_counts["Has External Link"].map({True: "External Link", False: "No External Link"})

# Streamlit UI
st.title("🔗 External Links Frequency Analysis")

# Pie Chart
fig = px.pie(
    external_link_counts,
    names="Has External Link",
    values="Count",
    title="Proportion of External vs. Non-External Posts",
    hole=0.4,  # Donut-style pie chart
)

st.plotly_chart(fig)


# Categorize posts as containing external links or not
df["has_external_link"] = df["url_overridden_by_dest"].notna()

# Group by Premium Status and calculate percentage of external link posts
premium_external_link = df.groupby("author_premium")["has_external_link"].mean().reset_index()

# Convert boolean values to labels
premium_external_link["author_premium"] = premium_external_link["author_premium"].map({True: "Premium User", False: "Non-Premium User"})
premium_external_link["has_external_link"] *= 100  # Convert to percentage

# Streamlit UI
st.title("💎 Premium Users vs. External Links")

# Bar Chart
fig = px.bar(
    premium_external_link,
    x="author_premium",
    y="has_external_link",
    text=premium_external_link["has_external_link"].round(2).astype(str) + "%",
    labels={"author_premium": "User Type", "has_external_link": "Percentage of External Link Posts"},
    title="External Link Usage by Premium vs. Non-Premium Users",
    color="author_premium",
)

# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! SECOND GRAPH !!!!!!!!!!!!!!!!!!!!!!!!

# st.plotly_chart(fig)



# Categorize posts as containing external links or not
df["has_external_link"] = df["url_overridden_by_dest"].notna()

# Keep relevant columns
df_filtered = df[["post_hint", "has_external_link"]].copy()

# Replace NaN values in post_hint with "Text"
df_filtered["post_hint"].fillna("Text", inplace=True)

# Group by post type and external link presence
post_type_analysis = df_filtered.groupby(["post_hint", "has_external_link"]).size().reset_index(name="count")

# Convert boolean values for external links to labels
post_type_analysis["has_external_link"] = post_type_analysis["has_external_link"].map({True: "Contains External Link", False: "No External Link"})

# Streamlit UI
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!THIRD GRAPH!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# st.title("🔗 External Links & Media Posts")

# # Stacked Bar Chart
# fig = px.bar(
#     post_type_analysis,
#     x="post_hint",
#     y="count",
#     color="has_external_link",
#     text="count",
#     labels={"post_hint": "Post Type", "count": "Number of Posts", "has_external_link": "External Link Presence"},
#     title="Distribution of External Links in Media & Text-Based Posts",
#     barmode="stack"
# )

# st.plotly_chart(fig)