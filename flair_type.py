import streamlit as st
import pandas as pd
import plotly.express as px
import streamlit as st
import pandas as pd
import plotly.express as px

# Load Data
@st.cache_data
def load_data():
    return pd.read_csv("cleaned_reddit_data.csv")

df = load_data()

# Main Title
st.title("📊 Flair Distribution")

# Flair Distribution
st.subheader("Flair Distribution: Count occurrences of link_flair_text")

# Count occurrences and remove "Unknown" flair
flair_counts = df["link_flair_text"].value_counts().reset_index()
flair_counts.columns = ["Flair", "Count"]
flair_counts = flair_counts[flair_counts["Flair"] != "Unknown"]  # Exclude "Unknown"

# Select Top 15 flairs for better readability
top_n = 15
flair_counts = flair_counts.head(top_n)

# Add "None Selected" option to the dropdown
options = ["None Selected"] + flair_counts["Flair"].tolist()
selected_flair = st.selectbox("Select a flair to highlight:", options)

# Add a color column to the dataframe
flair_counts["Color"] = flair_counts["Flair"].apply(lambda x: "Highlighted" if x == selected_flair else "Normal") if selected_flair != "None Selected" else "Normal"

# Plot Horizontal Bar Chart
fig = px.bar(
    flair_counts, 
    x="Count", 
    y="Flair", 
    orientation="h",  # Horizontal bar chart
    labels={"Flair": "Flair", "Count": "Count"},
    title=f"Top {top_n} Most Common Flairs",
    text="Count",  # Display count on bars
    color="Color",  # Use the new column for coloring
    color_discrete_map={"Highlighted": "red", "Normal": "blue"}  # Highlight selected flair
)

# Adjust figure size
fig.update_layout(
    height=600, width=800,
    margin=dict(l=100, r=50, t=50, b=50),
)

# Show chart
st.plotly_chart(fig)

# Post Size Analysis (Thumbnail Dimensions)

# Do Author Premium posts more
premium_counts = df["author_premium"].value_counts().reset_index()
premium_counts.columns = ["Premium User", "Post Count"]
premium_counts["Premium User"] = premium_counts["Premium User"].map({True: "Premium", False: "Non-Premium"})

st.title("📊 Premium User Engagement: Posting Frequency")

# Bar Chart
st.subheader("Bar Chart: Posts by Premium vs. Non-Premium Users")
fig_bar = px.bar(premium_counts, x="Premium User", y="Post Count", color="Premium User",
                 labels={"Premium User": "User Type", "Post Count": "Number of Posts"},
                 text_auto=True, title="Posting Frequency by Premium Status")
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! SECOND GRAPH !!!!!!!!!!!!!!!!!!!!!!
# st.plotly_chart(fig_bar)

# Pie Chart
st.subheader("Pie Chart: Percentage of Posts by Premium vs. Non-Premium Users")
fig_pie = px.pie(premium_counts, names="Premium User", values="Post Count",
                 title="Post Distribution by Premium Status")
st.plotly_chart(fig_pie)



# NSFW Content: Are Premium Users More Likely to Post NSFW?

# Map premium users to labels
df["Premium User"] = df["author_premium"].map({True: "Premium", False: "Non-Premium"})

