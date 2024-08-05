"""
Component function to render inference statistics
"""

import streamlit as st


def display_statistics(placeholder, statistics_text):
    with placeholder.container():
        if statistics_text:
            if "Generating structure in background" not in statistics_text:
                st.markdown(statistics_text + "\n\n---\n")
            else:
                st.markdown(statistics_text)
        else:
            placeholder.empty()
