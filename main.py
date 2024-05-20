import streamlit as st
from groq import Groq
import json
import os
from io import BytesIO

GROQ_API_KEY = os.environ.get("GROQ_API_KEY", None)

if 'api_key' not in st.session_state:
    st.session_state.api_key = GROQ_API_KEY

if 'groq' not in st.session_state:
    if GROQ_API_KEY:
        st.session_state.groq = Groq()

class Book:
    def __init__(self, structure):
        self.structure = structure
        self.contents = {title: "" for title in self.flatten_structure(structure)}
        self.placeholders = {title: st.empty() for title in self.flatten_structure(structure)}

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
        
        markdown_content = ""
        for title, content in structure.items():
            if self.contents[title].strip():  # Only include title if there is content
                markdown_content += f"{'#' * level} {title}\n{self.contents[title]}\n\n"
            if isinstance(content, dict):
                markdown_content += self.get_markdown_content(content, level + 1)
        return markdown_content

def create_markdown_file(content: str) -> BytesIO:
    """
    Create a Markdown file from the provided content.
    """
    markdown_file = BytesIO()
    markdown_file.write(content.encode('utf-8'))
    markdown_file.seek(0)
    return markdown_file

def generate_book_structure(prompt: str):
    completion = st.session_state.groq.chat.completions.create(
        model="llama3-70b-8192",
        messages=[
            {
                "role": "system",
                "content": "Write in JSON format:\n\n{\"Title of section goes here\":\"Description of section goes here\",\n\"Title of section goes here\":{\"Title of section goes here\":\"Description of section goes here\",\"Title of section goes here\":\"Description of section goes here\",\"Title of section goes here\":\"Description of section goes here\"}}"
            },
            {
                "role": "user",
                "content": f"Write a comprehensive structure, omiting common sections like a forward or author's note, for a long (>300 page) book on the following subject:\n\n<subject>{prompt}</subject>"
            }
        ],
        temperature=0.3,
        max_tokens=8000,
        top_p=1,
        stream=False,
        response_format={"type": "json_object"},
        stop=None,
    )

    return completion.choices[0].message.content

def generate_section(prompt: str):
    stream = st.session_state.groq.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {
                "role": "system",
                "content": "You are an expert writer. Generate a long, comprehensive, structured chapter for the section provided."
            },
            {
                "role": "user",
                "content": f"Generate a long, comprehensive, structured chapter for the following section:\n\n<section_title>{prompt}</section_title>"
            }
        ],
        temperature=0.3,
        max_tokens=8000,
        top_p=1,
        stream=True,
        stop=None,
    )

    for chunk in stream:
        resulting_tokens = chunk.choices[0].delta.content
        yield resulting_tokens

# Initialize
if 'button_disabled' not in st.session_state:
    st.session_state.button_disabled = False

if 'button_text' not in st.session_state:
    st.session_state.button_text = "Generate"

st.write("""
# Groqbook: Write full books using llama3 (8b and 70b) on Groq
""")

def disable():
    st.session_state.button_disabled = True

def enable():
    st.session_state.button_disabled = False

def empty_st():
    st.empty()

try:
    if st.button('End Generation and Download Book'):
        if "book" in st.session_state:
            markdown_file = create_markdown_file(st.session_state.book.get_markdown_content())
            st.download_button(
                label='Confirm Download',
                data=markdown_file,
                file_name='generated_book.txt',
                mime='text/plain'
            )
        else:
            raise ValueError("Please generate content first before downloading the book.")

    with st.form("groqform"):
        if not GROQ_API_KEY:
            groq_input_key = st.text_input("Enter your Groq API Key:", "gsk_yA...")

        topic_text = st.text_input("What do you want the book to be about?", "")

        submitted = st.form_submit_button(st.session_state.button_text,on_click=disable,disabled=st.session_state.button_disabled)

        if submitted:
            if len(topic_text)<10:
                raise ValueError("Book topic must be at least 10 characters long")

            st.session_state.button_disabled = True
            st.write("Generating structure in background....")

            if not GROQ_API_KEY:
                st.session_state.groq = Groq(api_key=groq_input_key)

            book_structure = generate_book_structure(topic_text)
            
            try:
                book_structure_json = json.loads(book_structure)
                book = Book(book_structure_json)
                
                if 'book' not in st.session_state:
                    st.session_state.book = book

                # Print the book structure to the terminal for debugging purposes
                print(json.dumps(book_structure_json, indent=2))

                st.session_state.book.display_structure()

                def stream_section_content(sections):
                    for title, content in sections.items():
                        if isinstance(content, str):
                            content_stream = generate_section(title+": "+content)
                            for chunk in content_stream:
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