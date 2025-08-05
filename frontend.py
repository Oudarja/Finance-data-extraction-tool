import streamlit as st
import pandas as pd
from llm_backend import  extract_financial_data

# Set page layout to wide
st.set_page_config(layout="wide")

# Layout using columns
left_col, right_col = st.columns([2, 2])

# Left column - article input and extract button
with left_col:
    st.header("📄 Enter News Article")
    article = st.text_area("Paste the article below:", height=300)
    extract_button = st.button("Extract")

# Right column - show extracted info
with right_col:
    st.header("📊 Extracted Financial Data")
    if extract_button and article:
        extracted_data = extract_financial_data(article)
        st.table(extracted_data)
    elif not article and extract_button:
        st.warning("Please enter an article before clicking Extract.")

