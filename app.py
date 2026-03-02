import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

st.title("SentProp Historical Sentiment Tracker")

# User input
term = st.text_input("Enter a word to track:", value="silly").lower()

if term:
    files = sorted(glob.glob("*.tsv"))
    years = []
    polarities = []

    # Data extraction
    for file in files:
        try:
            year = int(os.path.basename(file).split('.')[0])
            df = pd.read_csv(file, sep='\t', names=['word', 'polarity', 'std_dev'])
            
            row = df[df['word'] == term]
            if not row.empty:
                years.append(year)
                polarities.append(row['polarity'].values[0])
        except Exception:
            continue

    # Visualization
    if years:
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(years, polarities, marker='o', linestyle='-', color='#1f77b4')
        ax.set_title(f"Sentiment Shift of '{term.capitalize()}' (1850-2000)")
        ax.set_xlabel("Year")
        ax.set_ylabel("Polarity Score")
        ax.grid(True, alpha=0.3)
        
        st.pyplot(fig)
    else:
        st.warning(f"No data found for the word: '{term}'")

# Instructions to run: 
# Save as app.py and run 'streamlit run app.py' in your terminal.
