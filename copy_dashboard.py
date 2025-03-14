import streamlit as st
import pandas as pd
import plotly.express as px
import streamlit as st
import pandas as pd
import plotly.express as px
import os
import tabulate
import streamlit as st
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_experimental.agents import create_csv_agent


# Create a layout with seven sections
st.set_page_config(layout="wide")

# Remove extra padding/margin at the top
# st.markdown("""
#     <style>
#         .block-container {
            
#         }
#         .scroll-container {
#             height: 100vh;
#             overflow-y: auto;
#         }
#     </style>
# """, unsafe_allow_html=True)

# First section (col1 and col2 side by side, full width)



@st.cache_data
def load_data():
    return pd.read_csv("cleaned_reddit_data.csv")

df = load_data()


section_style = "border: 2px solid white; padding: 10px; border-radius: 5px; margin-bottom: 10px;"


st.markdown("</div>", unsafe_allow_html=True)




st.subheader("Count of Flair Type Occurrences")

# Count occurrences and remove "Unknown" flair
flair_counts = df["link_flair_text"].value_counts().reset_index()
flair_counts.columns = ["Flair", "Count"]
flair_counts = flair_counts[flair_counts["Flair"] != "Unknown"]  # Exclude "Unknown"

# Initialize session state for `top_n_input` only if it is not set
if "top_n_input_flairs" not in st.session_state:
    st.session_state.top_n_input_flairs = 10  # Default value

# User input for number of top flairs
top_n = st.number_input("Select number of top flairs to display", 
                        min_value=1, 
                        max_value=136, 
                        value=10, 
                        step=1, 
                        key="top_n_input_flairs")

# Select a flair to highlight
options = ["None Selected"] + flair_counts["Flair"].tolist()
selected_flair = st.selectbox("Select a flair to highlight:", options, key="flair_select_flairs")

# Get top N flairs
top_flairs = flair_counts.head(top_n)

# If a flair is selected and it's not in top N, increase N and include it
if selected_flair != "None Selected" and selected_flair not in top_flairs["Flair"].values:
    selected_row = flair_counts[flair_counts["Flair"] == selected_flair]
    
    if not selected_row.empty:
        # Increase top_n and add the selected flair if needed
        top_n += 1
        top_flairs = pd.concat([top_flairs, selected_row]).drop_duplicates().reset_index(drop=True)

# Assign colors: Red for selected, Blue for others
top_flairs["Color"] = top_flairs["Flair"].apply(lambda x: "Highlighted" if x == selected_flair else "Normal")

# Update title dynamically based on `top_n`
title_text = f"Top {len(top_flairs)} Most Common Flairs"

# Plot Horizontal Bar Chart
fig = px.bar(
    top_flairs, 
    x="Count", 
    y="Flair", 
    orientation="h",  # Horizontal bar chart
    labels={"Flair": "Flair", "Count": "Count"},
    title=title_text,
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


col1, col2 = st.columns([1, 1])









with col1:
    # st.markdown(f"""
    # <div style='{section_style}'>
    #     <h3>Section 1</h3>
    #     <p>This section covers the full screen width side by side with Section 2.</p>
    # </div>
    # """, unsafe_allow_html=True)

    premium_counts = df["author_premium"].value_counts().reset_index()
    premium_counts.columns = ["Premium User", "Post Count"]
    premium_counts["Premium User"] = premium_counts["Premium User"].map({True: "Premium", False: "Non-Premium"})

    # st.title("📊 Premium User Engagement: Posting Frequency")

    # Bar Chart
    # st.subheader("Bar Chart: Posts by Premium vs. Non-Premium Users")
    fig_bar = px.bar(premium_counts, x="Premium User", y="Post Count", color="Premium User",
                    labels={"Premium User": "User Type", "Post Count": "Number of Posts"},
                    text_auto=True, title="Posting Frequency by Premium Status")
    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! SECOND GRAPH !!!!!!!!!!!!!!!!!!!!!!
    # st.plotly_chart(fig_bar)

    # Pie Chart
    # st.subheader("Pie Chart: Percentage of Posts by Premium vs. Non-Premium Users")
    fig_pie = px.pie(premium_counts, names="Premium User", values="Post Count",
                    title="Percentage of Posts by Premium and Non-Premium Users")
    st.plotly_chart(fig_pie)



    # NSFW Content: Are Premium Users More Likely to Post NSFW?

    # Map premium users to labels
    df["Premium User"] = df["author_premium"].map({True: "Premium", False: "Non-Premium"})



with col2:
    # st.markdown(f"""
    # <div style='{section_style}'>
    #     <h3>Section 2</h3>
    #     <p>This section appears beside Section 1.</p>
    # </div>
    # """, unsafe_allow_html=True)

    df["has_external_link"] = df["url_overridden_by_dest"].notna()

    # Count the occurrences
    external_link_counts = df["has_external_link"].value_counts().reset_index()
    external_link_counts.columns = ["Has External Link", "Count"]

    # Convert boolean values to labels
    external_link_counts["Has External Link"] = external_link_counts["Has External Link"].map({True: "External Link", False: "No External Link"})

    # Streamlit UI
    # st.title("🔗 External Links Frequency Analysis")

    # Pie Chart
    fig = px.pie(
        external_link_counts,
        names="Has External Link",
        values="Count",
        title="Proportion of External vs. Non-External Link-Containing Posts",
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
    # st.title("💎 Premium Users vs. External Links")

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


# Scrollable section (col3 and col4 side by side when scrolled)
st.markdown("<div class='scroll-container'>", unsafe_allow_html=True)
col3, col4 = st.columns([1, 1])

with col3:
    # st.markdown(f"""
    # <div style='{section_style}'>
    #     <h3>Section 3</h3>
    #     <p>This section appears in a scrollable area alongside Section 4.</p>
    # </div>
    # """, unsafe_allow_html=True)

    # st.markdown(f"""
    # <div style='{section_style}'>
    #     <h3>Section 5</h3>
    #     <p>This section appears below Section 3.</p>
    # </div>
    # """, unsafe_allow_html=True)

    df["aspect_ratio"] = df["thumbnail_width"] / df["thumbnail_height"]

    # Plot Histogram
    fig = px.histogram(df, x="aspect_ratio", title="Distribution of Thumbnail Aspect Ratios (Width-to-Height)", nbins=20)
    st.plotly_chart(fig) 



    # 2) Most Common Thumbnail Sizes

    size_counts = df.groupby(["thumbnail_width", "thumbnail_height"]).size().reset_index(name="count")

    fig = px.bar(size_counts.sort_values("count", ascending=False).head(10),
                x="thumbnail_width", y="count", color="thumbnail_height",
                title="Top 10 Most Common Thumbnail Sizes",
                labels={"thumbnail_width": "Width", "count": "Frequency"})
    # st.plotly_chart(fig)


    # 3) Post Size by Flair
    df["thumbnail_area"] = df["thumbnail_width"] * df["thumbnail_height"]
    flair_avg_size = df.groupby("link_flair_text")["thumbnail_area"].mean().reset_index()

    fig = px.bar(flair_avg_size.sort_values("thumbnail_area", ascending=False),
                x="link_flair_text", y="thumbnail_area",
                title="📊 Average Thumbnail Size by Flair",
                labels={"link_flair_text": "Flair", "thumbnail_area": "Avg. Size"})
    # st.plotly_chart(fig)


    # Do Premium Users Upload Larger Thumbnails?

    fig = px.box(df, x="author_premium", y="thumbnail_area",
                title="📊 Thumbnail Area Distribution (Premium vs. Non-Premium Users)",
                labels={"author_premium": "Premium User", "thumbnail_area": "Thumbnail Area"})
    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! THIRD GRAPH  !!!!!!!!!!!!!!!
    # st.plotly_chart(fig)










with col4:
    df["aspect_ratio"] = df["thumbnail_width"] / df["thumbnail_height"]

    # Plot Histogram
    fig = px.histogram(df, x="aspect_ratio", title="📏 Distribution of Thumbnail Aspect Ratios", nbins=20)
    # st.plotly_chart(fig) 



    # 2) Most Common Thumbnail Sizes

    size_counts = df.groupby(["thumbnail_width", "thumbnail_height"]).size().reset_index(name="count")

    fig = px.bar(size_counts.sort_values("count", ascending=False).head(10),
                x="thumbnail_width", y="count", color="thumbnail_height",
                title="Top 10 Most Common Thumbnail Sizes",
                labels={"thumbnail_width": "Width", "count": "Frequency"})
    st.plotly_chart(fig)


    # 3) Post Size by Flair
    df["thumbnail_area"] = df["thumbnail_width"] * df["thumbnail_height"]
    flair_avg_size = df.groupby("link_flair_text")["thumbnail_area"].mean().reset_index()

    fig = px.bar(flair_avg_size.sort_values("thumbnail_area", ascending=False),
                x="link_flair_text", y="thumbnail_area",
                title="📊 Average Thumbnail Size by Flair",
                labels={"link_flair_text": "Flair", "thumbnail_area": "Avg. Size"})
    # st.plotly_chart(fig)


    # Do Premium Users Upload Larger Thumbnails?

    fig = px.box(df, x="author_premium", y="thumbnail_area",
                title="📊 Thumbnail Area Distribution (Premium vs. Non-Premium Users)",
                labels={"author_premium": "Premium User", "thumbnail_area": "Thumbnail Area"})
    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! THIRD GRAPH  !!!!!!!!!!!!!!!
    # st.plotly_chart(fig)



st.markdown("<div class='scroll-container'>", unsafe_allow_html=True)
col5, col6 = st.columns([1, 1])

with col5:
    # Initialize session state for `top_n_input` only if it is not set
    if "top_n_input" not in st.session_state:
        st.session_state.top_n_input = 10  # Default value

    # Compute `thumbnail_area`
    df["thumbnail_area"] = df["thumbnail_width"] * df["thumbnail_height"]

    # Group by `link_flair_text` and compute the average `thumbnail_area`
    flair_avg_size = df.groupby("link_flair_text", as_index=False)["thumbnail_area"].mean()

    # Get all unique flair options and add "None Selected"
    options = ["None Selected"] + flair_avg_size["link_flair_text"].tolist()

    # User input for number of top flairs
    top_n = st.number_input("Select number of top flairs to display", 
                            min_value=1, 
                            max_value=136, 
                            # value=st.session_state.top_n_input, 
                            value=10, 
                            step=1, 
                            key="top_n_input")

    # Select a flair to highlight
    selected_flair = st.selectbox("Select a flair to highlight:", options, key="flair_select")

    # Get top N flairs
    top_flairs = flair_avg_size.sort_values("thumbnail_area", ascending=False).head(top_n)

    # If a flair is selected and it's not in top N, increase N and include it
    if selected_flair != "None Selected" and selected_flair not in top_flairs["link_flair_text"].values:
        selected_row = flair_avg_size[flair_avg_size["link_flair_text"] == selected_flair]
        
        if not selected_row.empty:
            # Increase top_n but **do not modify session state directly** after the widget is instantiated
            top_n += 1
            top_flairs = pd.concat([top_flairs, selected_row]).drop_duplicates().reset_index(drop=True)

    # Assign colors: Red for selected, Blue for others
    top_flairs["color"] = top_flairs["link_flair_text"].apply(lambda x: "red" if x == selected_flair else "blue")

    # Update title dynamically based on `top_n`
    title_text = f"Top {len(top_flairs)} Flair Types by Average Thumbnail Size"

    # Plot using Plotly
    fig = px.bar(top_flairs,
                 x="link_flair_text", y="thumbnail_area",
                 title=title_text,
                 labels={"link_flair_text": "Flair", "thumbnail_area": "Avg. Size"},
                 color="color",
                 color_discrete_map={"red": "red", "blue": "blue"})  # Assign colors

    # Rotate labels for better readability
    fig.update_layout(xaxis_tickangle=-45, margin=dict(l=10, r=10, b=150, t=30))

    # Display plot in Streamlit
    st.plotly_chart(fig)





with col6:
    df = df[df["over_18"].notna()]

    # Title
    # st.title("NSFW Content Proportion")

    # Calculate NSFW Percentage
    nsfw_counts = df["over_18"].value_counts(normalize=True) * 100
    nsfw_df = pd.DataFrame({"Category": nsfw_counts.index, "Percentage": nsfw_counts.values})

    # Pie Chart
    fig = px.pie(nsfw_df, names="Category", values="Percentage", title="Proportion of NSFW vs. SFW Content")
    st.plotly_chart(fig)






load_dotenv()

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

# Specify the path to your CSV file
CSV_FILE_PATH = "cleaned_reddit_data.csv"  # Replace with the relative or absolute path

# st.set_page_config(page_title="ASK YOUR CSV")
st.title("ASK YOUR DATA")
st.header("ASK YOUR CSV")

# Load the CSV file automatically from the project directory
if os.path.exists(CSV_FILE_PATH):
    try:
        # Try opening the file with UTF-8 encoding (or other common encodings if needed)
        with open(CSV_FILE_PATH, "r", encoding="utf-8") as f:
            csv = f.read()  # Read the CSV content
    except UnicodeDecodeError:
        # If UTF-8 fails, attempt to read with a different encoding like 'latin1'
        with open(CSV_FILE_PATH, "r", encoding="latin1") as f:
            csv = f.read()  # Read the CSV content
        
    agent = create_csv_agent(
        ChatGroq(
            model="llama3-70b-8192",
            temperature=0), 
        CSV_FILE_PATH,  # Pass the file path instead of the file object
        verbose=True, 
        handle_parsing_errors=True,
        allow_dangerous_code=True,
    )

    user_question = st.text_input("Ask a question about your CSV: ")

    if user_question is not None and user_question != "":
        with st.spinner(text="In progress..."):
            st.write(agent.run(user_question))
else:
    st.error(f"CSV file not found at {CSV_FILE_PATH}")

