import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

st.title("SentProp Historical Sentiment Tracker")

# Category selection
category = st.selectbox("Choose a category:", ["frequent_words", "adjectives"])

# User input
term = st.text_input(f"Enter a word from {category}:", value="silly").lower()

if term:
    # Point to the specific folder
    folder_path = os.path.join(category, "*.tsv")
    files = sorted(glob.glob(folder_path))
    
    years, polarities = [], []

    for file in files:
        try:
            # Handle filename extraction based on your OS path
            year_str = os.path.basename(file).split('.')[0]
            year = int(year_str)
            
            df = pd.read_csv(file, sep='\t', names=['word', 'polarity', 'std_dev'])
            row = df[df['word'] == term]
            
            if not row.empty:
                years.append(year)
                polarities.append(row['polarity'].values[0])
        except (ValueError, pd.errors.EmptyDataError):
            continue

    if years:
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(years, polarities, marker='o', markersize=4, linewidth=2, color='#2ca02c')
        ax.axhline(0, color='black', lw=1, ls='--') # Zero line for context
        ax.set_title(f"Sentiment Shift: '{term.capitalize()}'")
        ax.set_xlabel("Year")
        ax.set_ylabel("Polarity Score")
        ax.grid(True, alpha=0.3)
        
        st.pyplot(fig)
    else:
        st.warning(f"No data found for '{term}' in the '{category}' folder.")

# Note: Ensure your local folder structure matches:
# /app.py
# /frequent_words/*.tsv
# /adjectives/*.tsv
