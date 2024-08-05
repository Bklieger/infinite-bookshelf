"""
Component function to render basic prompt input form
"""

import streamlit as st


def render_groq_form(on_submit, button_disabled=False, button_text="Generate"):
    with st.form("groqform"):
        groq_input_key = (
            st.text_input("Enter your Groq API Key (gsk_yA...):", "", type="password")
            if not st.session_state.get("api_key")
            else None
        )

        topic_text = st.text_input(
            "What do you want the book to be about?",
            value="",
            help="Enter the main topic or title of your book",
        )

        additional_instructions = st.text_area(
            "Additional Instructions (optional)",
            help="Provide any specific guidelines or preferences for the book's content",
            placeholder="E.g., 'Focus on beginner-friendly content', 'Include case studies', etc.",
            value="",
        )

        submitted = st.form_submit_button(
            button_text,
            on_click=on_submit,
            disabled=button_disabled,
        )

        return submitted, groq_input_key, topic_text, additional_instructions
