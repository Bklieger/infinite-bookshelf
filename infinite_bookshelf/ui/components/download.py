"""
Component function to download button
"""

import streamlit as st
from ...tools import create_markdown_file, create_pdf_file


def render_download_buttons(book):
    if book:
        # Create markdown file
        markdown_file = create_markdown_file(book.get_markdown_content())
        st.download_button(
            label="Download Text",
            data=markdown_file,
            file_name=f"{book.book_title}.txt",
            mime="text/plain",
        )

        # Create pdf file (styled)
        pdf_file = create_pdf_file(book.get_markdown_content())
        st.download_button(
            label="Download PDF",
            data=pdf_file,
            file_name=f"{book.book_title}.pdf",
            mime="application/pdf",
        )
    else:
        st.error("Please generate content first before downloading the book.")
