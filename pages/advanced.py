# 1: Import libraries
import streamlit as st
from groq import Groq
import json

from infinite_bookshelf.agents import (
    generate_section,
    generate_book_structure,
    generate_book_title,
)
from infinite_bookshelf.inference import GenerationStatistics
from infinite_bookshelf.tools import create_markdown_file, create_pdf_file
from infinite_bookshelf.ui.components import (
    render_groq_form,
    render_advanced_groq_form,
    display_statistics,
    render_download_buttons,
)
from infinite_bookshelf.ui import Book, load_return_env, ensure_states


# 2: Initialize env variables and session states
GROQ_API_KEY = load_return_env(["GROQ_API_KEY"])["GROQ_API_KEY"]

states = {
    "api_key": GROQ_API_KEY,
    "button_disabled": False,
    "button_text": "Generate",
    "statistics_text": "",
    "book_title": "",
}

if GROQ_API_KEY:
    states["groq"] = (
        Groq()
    )  # Define Groq provider if API key provided. Otherwise defined later after API key is provided.

ensure_states(states)


# 3: Define Streamlit page structure and functionality
st.write(
    """
# Infinite Bookshelf: Write full books using Llama on Groq
"""
)


def disable():
    st.session_state.button_disabled = True


def enable():
    st.session_state.button_disabled = False


def empty_st():
    st.empty()


try:
    if st.button("End Generation and Download Book"):
        if "book" in st.session_state:
            render_download_buttons(st.session_state.get("book"))

    (
        submitted,
        groq_input_key,
        topic_text,
        additional_instructions,
        writing_style,
        complexity_level,
        seed_content,
        uploaded_file,
        title_agent_model,
        structure_agent_model,
        section_agent_model,
    ) = render_advanced_groq_form(
        on_submit=disable,
        button_disabled=st.session_state.button_disabled,
        button_text=st.session_state.button_text,
    )

    # New content for advanced mode
    additional_section_writer_prompt = "The book chapters should be comprehensive. The writing should be: \nEngaging and tailored to the specified writing style, tone, and complexity level. \nWell-structured with clear subheadings, paragraphs, and transitions. \nRich in relevant examples, analogies, and explanations. \nConsistent with provided seed content and additional instructions. \nFocused on delivering value through insightful analysis and information. \nFactually accurate based on the latest available information. \nCreative, offering unique perspectives or thought-provoking ideas. \nEnsure each section flows logically, maintaining coherence throughout the chapter."
    advanced_settings_prompt = f"Use the following parameters:\nWriting Style: {writing_style}\nComplexity Level: {complexity_level}"
    total_seed_content = ""

    # Fill total_seed_content
    if seed_content:
        total_seed_content += seed_content
    if uploaded_file:
        total_seed_content += uploaded_file.read().decode("utf-8")
    if total_seed_content != "":
        total_seed_content = f"The user has provided seed content for context. Develop the structure and content around the provided seed: <seed>{total_seed_content}</seed>"

    if submitted:
        if len(topic_text) < 10:
            raise ValueError("Book topic must be at least 10 characters long")

        st.session_state.button_disabled = True
        st.session_state.statistics_text = (
            "Generating book title and structure in background...."
        )

        placeholder = st.empty()
        display_statistics(
            placeholder=placeholder, statistics_text=st.session_state.statistics_text
        )

        if not GROQ_API_KEY:
            st.session_state.groq = Groq(api_key=groq_input_key)

        # Step 1: Generate book structure using structure_writer agent
        additional_instructions_prompt = (
            additional_instructions + advanced_settings_prompt
        )
        if total_seed_content != "":
            additional_instructions_prompt += "\n" + total_seed_content

        large_model_generation_statistics, book_structure = generate_book_structure(
            prompt=topic_text,
            additional_instructions=additional_instructions_prompt,
            model=structure_agent_model,
            groq_provider=st.session_state.groq,
            long=True # Use longer version in advanced
        )

        # Step 2: Generate book title using title_writer agent
        st.session_state.book_title = generate_book_title(
            prompt=topic_text,
            model=title_agent_model,
            groq_provider=st.session_state.groq,
        )

        st.write(f"## {st.session_state.book_title}")

        total_generation_statistics = GenerationStatistics(
            model_name=section_agent_model
        )

        # Step 3: Generate book section content using section_writer agent
        try:
            book_structure_json = json.loads(book_structure)
            book = Book(st.session_state.book_title, book_structure_json)

            if "book" not in st.session_state:
                st.session_state.book = book

            # Print the book structure to the terminal to show structure
            print(json.dumps(book_structure_json, indent=2))

            st.session_state.book.display_structure()

            def stream_section_content(sections):
                for title, content in sections.items():
                    if isinstance(content, str):
                        additional_instructions_prompt = f"{additional_section_writer_prompt}\n{additional_instructions}\n{advanced_settings_prompt}"
                        if total_seed_content != "":
                            additional_instructions_prompt += "\n" + total_seed_content

                        content_stream = generate_section(
                            prompt=(title + ": " + content),
                            additional_instructions=additional_instructions_prompt,
                            model=section_agent_model,
                            groq_provider=st.session_state.groq,
                        )
                        for chunk in content_stream:
                            # Check if GenerationStatistics data is returned instead of str tokens
                            chunk_data = chunk
                            if type(chunk_data) == GenerationStatistics:
                                total_generation_statistics.add(chunk_data)

                                st.session_state.statistics_text = str(
                                    total_generation_statistics
                                )
                                display_statistics(
                                    placeholder=placeholder,
                                    statistics_text=st.session_state.statistics_text,
                                )

                            elif chunk != None:
                                st.session_state.book.update_content(title, chunk)
                    elif isinstance(content, dict):
                        stream_section_content(content)

            stream_section_content(book_structure_json)

        except json.JSONDecodeError:
            st.error("Failed to decode the book structure. Please try again.")


except Exception as e:
    st.session_state.button_disabled = False
    st.error(e)

    if st.button("Clear"):
        st.rerun()
