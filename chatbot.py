import os
import tabulate
import streamlit as st
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_experimental.agents import create_csv_agent

load_dotenv()

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

# Specify the path to your CSV file
CSV_FILE_PATH = "cleaned_reddit_data.csv"  # Replace with the relative or absolute path

def main():
    st.set_page_config(page_title="ASK YOUR CSV")
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

if __name__ == "__main__":
    main()
