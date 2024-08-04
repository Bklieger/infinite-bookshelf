import streamlit as st
from groq import Groq
import json
import os
from markdown import markdown
from weasyprint import HTML, CSS
from dotenv import load_dotenv

from infinite_bookshelf.agents import generate_section, generate_book_structure, generate_book_title
from infinite_bookshelf.inference import GenerationStatistics
from infinite_bookshelf.tools import create_markdown_file, create_pdf_file

# load .env file to environment
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY", None)

if "api_key" not in st.session_state:
    st.session_state.api_key = GROQ_API_KEY

if "groq" not in st.session_state:
    if GROQ_API_KEY:
        st.session_state.groq = Groq()

class Book:
    def __init__(self, book_title, structure):
        self.book_title = book_title
        self.structure = structure
        self.contents = {title: "" for title in self.flatten_structure(structure)}
        self.placeholders = {title: st.empty() for title in self.flatten_structure(structure)}
        st.markdown(f"# {self.book_title}")
        st.markdown("## Generating the following:")
        toc_columns = st.columns(4)
        self.display_toc(self.structure, toc_columns)
        st.markdown("---")

    def flatten_structure(self, structure):
        sections = []
        for title, content in structure.items():
            sections.append(title)
            if isinstance(content, dict):
                sections.extend(self.flatten_structure(content))
        return sections

    def update_content(self, title, new_content):
        try:
            self.contents[title] += new_content
            self.display_content(title)
        except TypeError as e:
            pass

    def display_content(self, title):
        if self.contents[title].strip():
            self.placeholders[title].markdown(f"## {title}\n{self.contents[title]}")

    def display_structure(self, structure=None, level=1):
        if structure is None:
            structure = self.structure
            
        for title, content in structure.items():
            if self.contents[title].strip():  # Only display title if there is content
                st.markdown(f"{'#' * level} {title}")
                self.placeholders[title].markdown(self.contents[title])
            if isinstance(content, dict):
                self.display_structure(content, level + 1)

    def display_toc(self, structure, columns, level=1, col_index=0):
        for title, content in structure.items():
            with columns[col_index % len(columns)]:
                st.markdown(f"{' ' * (level-1) * 2}- {title}")
            col_index += 1
            if isinstance(content, dict):
                col_index = self.display_toc(content, columns, level + 1, col_index)
        return col_index

    def get_markdown_content(self, structure=None, level=1):
        """
        Returns the markdown styled pure string with the contents.
        """
        if structure is None:
            structure = self.structure
        
        if level==1:
            markdown_content = f"# {self.book_title}\n\n"
            
        else:
            markdown_content = ""
        
        for title, content in structure.items():
            if self.contents[title].strip():  # Only include title if there is content
                markdown_content += f"{'#' * level} {title}\n{self.contents[title]}\n\n"
            if isinstance(content, dict):
                markdown_content += self.get_markdown_content(content, level + 1)
        return markdown_content


# Initialize
if "button_disabled" not in st.session_state:
    st.session_state.button_disabled = False

if "button_text" not in st.session_state:
    st.session_state.button_text = "Generate"

if "statistics_text" not in st.session_state:
    st.session_state.statistics_text = ""

if 'book_title' not in st.session_state:
    st.session_state.book_title = ""

st.write(
    """
# Infinite Bookshelf: Write full books using llama3 (8b and 70b) on Groq
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
            # Create markdown file
            markdown_file = create_markdown_file(
                st.session_state.book.get_markdown_content()
            )
            st.download_button(
                label="Download Text",
                data=markdown_file,
                file_name=f'{st.session_state.book_title}.txt',
                mime='text/plain'
            )

            # Create pdf file (styled)
            pdf_file = create_pdf_file(st.session_state.book.get_markdown_content())
            st.download_button(
                label="Download PDF",
                data=pdf_file,
                file_name=f'{st.session_state.book_title}.pdf',
                mime='application/pdf'
            )
        else:
            raise ValueError("Please generate content first before downloading the book.")

    with st.form("groqform"):
        if not GROQ_API_KEY:
            groq_input_key = st.text_input(
                "Enter your Groq API Key (gsk_yA...):", "", type="password"
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

        # Generate button
        submitted = st.form_submit_button(
            st.session_state.button_text,
            on_click=disable,
            disabled=st.session_state.button_disabled,
        )

        # Statistics
        placeholder = st.empty()

        def display_statistics():
            with placeholder.container():
                if st.session_state.statistics_text:
                    if (
                        "Generating structure in background"
                        not in st.session_state.statistics_text
                    ):
                        st.markdown(
                            st.session_state.statistics_text + "\n\n---\n"
                        )  # Format with line if showing statistics
                    else:
                        st.markdown(st.session_state.statistics_text)
                else:
                    placeholder.empty()

        if submitted:
            if len(topic_text) < 10:
                raise ValueError("Book topic must be at least 10 characters long")

            st.session_state.button_disabled = True
            st.session_state.statistics_text = "Generating book title and structure in background...."
            display_statistics()

            if not GROQ_API_KEY:
                st.session_state.groq = Groq(api_key=groq_input_key)

            large_model_generation_statistics, book_structure = generate_book_structure(
                prompt=topic_text,
                additional_instructions=additional_instructions,
                model="llama3-70b-8192", 
                groq_provider=st.session_state.groq
            )
            # Generate AI book title
            st.session_state.book_title = generate_book_title(
                prompt=topic_text,
                model="llama3-70b-8192", 
                groq_provider=st.session_state.groq
            )
            st.write(f"## {st.session_state.book_title}")

            total_generation_statistics = GenerationStatistics(
                model_name="llama3-8b-8192"
            )

            try:
                book_structure_json = json.loads(book_structure)
                book = Book(st.session_state.book_title, book_structure_json)
                
                if 'book' not in st.session_state:
                    st.session_state.book = book

                # Print the book structure to the terminal to show structure
                print(json.dumps(book_structure_json, indent=2))

                st.session_state.book.display_structure()
    
                def stream_section_content(sections):
                    for title, content in sections.items():
                        if isinstance(content, str):
                            content_stream = generate_section(
                                prompt=(title + ": " + content), additional_instructions=additional_instructions, model="llama3-8b-8192", groq_provider=st.session_state.groq,
                            )
                            for chunk in content_stream:
                                # Check if GenerationStatistics data is returned instead of str tokens
                                chunk_data = chunk
                                if type(chunk_data) == GenerationStatistics:
                                    total_generation_statistics.add(chunk_data)

                                    st.session_state.statistics_text = str(
                                        total_generation_statistics
                                    )
                                    display_statistics()

                                elif chunk != None:
                                    st.session_state.book.update_content(title, chunk)
                        elif isinstance(content, dict):
                            stream_section_content(content)

                stream_section_content(book_structure_json)

            except json.JSONDecodeError:
                st.error("Failed to decode the book structure. Please try again.")

            enable()

except Exception as e:
    st.session_state.button_disabled = False
    st.error(e)

    if st.button("Clear"):
        st.rerun()
