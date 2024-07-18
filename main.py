import streamlit as st
from groq import Groq
import json
import os
from io import BytesIO
from markdown import markdown
from weasyprint import HTML, CSS
from dotenv import load_dotenv

# load .env file to environment
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY", None)

if "api_key" not in st.session_state:
    st.session_state.api_key = GROQ_API_KEY

if "groq" not in st.session_state:
    if GROQ_API_KEY:
        st.session_state.groq = Groq()


# Initialize
if "button_disabled" not in st.session_state:
    st.session_state.button_disabled = False

if "button_text" not in st.session_state:
    st.session_state.button_text = "Generate"

if "statistics_text" not in st.session_state:
    st.session_state.statistics_text = ""

if "book_title" not in st.session_state:
    st.session_state.book_title = ""

# st.write(
#     """
# # Groqbook: Write full books using llama3 (8b and 70b) on Groq
# """
# )

st.set_page_config(page_title="GroqBook", page_icon="📚")

st.title("Groqbook: Write full books using llama3 (8b and 70b) on Groq")


class GenerationStatistics:
    def __init__(
        self,
        input_time=0,
        output_time=0,
        input_tokens=0,
        output_tokens=0,
        total_time=0,
        model_name="llama3-8b-8192",
    ):
        self.input_time = input_time
        self.output_time = output_time
        self.input_tokens = input_tokens
        self.output_tokens = output_tokens
        self.total_time = (
            total_time  # Sum of queue, prompt (input), and completion (output) times
        )
        self.model_name = model_name

    def get_input_speed(self):
        """
        Tokens per second calculation for input
        """
        if self.input_time != 0:
            return self.input_tokens / self.input_time
        else:
            return 0

    def get_output_speed(self):
        """
        Tokens per second calculation for output
        """
        if self.output_time != 0:
            return self.output_tokens / self.output_time
        else:
            return 0

    def add(self, other):
        """
        Add statistics from another GenerationStatistics object to this one.
        """
        if not isinstance(other, GenerationStatistics):
            raise TypeError("Can only add GenerationStatistics objects")

        self.input_time += other.input_time
        self.output_time += other.output_time
        self.input_tokens += other.input_tokens
        self.output_tokens += other.output_tokens
        self.total_time += other.total_time

    def __str__(self):
        return (
            f"\n## {self.get_output_speed():.2f} T/s ⚡\nRound trip time: {self.total_time:.2f}s  Model: {self.model_name}\n\n"
            f"| Metric          | Input          | Output          | Total          |\n"
            f"|-----------------|----------------|-----------------|----------------|\n"
            f"| Speed (T/s)     | {self.get_input_speed():.2f}            | {self.get_output_speed():.2f}            | {(self.input_tokens + self.output_tokens) / self.total_time if self.total_time != 0 else 0:.2f}            |\n"
            f"| Tokens          | {self.input_tokens}            | {self.output_tokens}            | {self.input_tokens + self.output_tokens}            |\n"
            f"| Inference Time (s) | {self.input_time:.2f}            | {self.output_time:.2f}            | {self.total_time:.2f}            |"
        )


class Book:
    def __init__(self, book_title, structure):
        self.book_title = book_title
        self.structure = structure
        self.contents = {title: "" for title in self.flatten_structure(structure)}
        self.placeholders = {
            title: st.empty() for title in self.flatten_structure(structure)
        }
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

        if level == 1:
            markdown_content = f"# {self.book_title}\n\n"

        else:
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
    markdown_file.write(content.encode("utf-8"))
    markdown_file.seek(0)
    return markdown_file


def create_pdf_file(content: str) -> BytesIO:
    """
    Create a PDF file from the provided Markdown content.
    Converts Markdown to styled HTML, then HTML to PDF.
    """

    html_content = markdown(content, extensions=["extra", "codehilite"])

    styled_html = f"""
    <html>
        <head>
            <style>
                @page {{
                    margin: 2cm;
                }}
                body {{
                    font-family: Arial, sans-serif;
                    line-height: 1.6;
                    font-size: 12pt;
                }}
                h1, h2, h3, h4, h5, h6 {{
                    color: #333366;
                    margin-top: 1em;
                    margin-bottom: 0.5em;
                }}
                p {{
                    margin-bottom: 0.5em;
                }}
                code {{
                    background-color: #f4f4f4;
                    padding: 2px 4px;
                    border-radius: 4px;
                    font-family: monospace;
                    font-size: 0.9em;
                }}
                pre {{
                    background-color: #f4f4f4;
                    padding: 1em;
                    border-radius: 4px;
                    white-space: pre-wrap;
                    word-wrap: break-word;
                }}
                blockquote {{
                    border-left: 4px solid #ccc;
                    padding-left: 1em;
                    margin-left: 0;
                    font-style: italic;
                }}
                table {{
                    border-collapse: collapse;
                    width: 100%;
                    margin-bottom: 1em;
                }}
                th, td {{
                    border: 1px solid #ddd;
                    padding: 8px;
                    text-align: left;
                }}
                th {{
                    background-color: #f2f2f2;
                }}
                input, textarea {{
                    border-color: #4A90E2 !important;
                }}
            </style>
        </head>
        <body>
            {html_content}
        </body>
    </html>
    """

    pdf_buffer = BytesIO()
    HTML(string=styled_html).write_pdf(pdf_buffer)
    pdf_buffer.seek(0)

    return pdf_buffer


def generate_book_title(prompt: str):
    """
    Generate a book title using AI.
    """
    completion = st.session_state.groq.chat.completions.create(
        model="llama3-70b-8192",
        messages=[
            {
                "role": "system",
                "content": "Generate suitable book titles for the provided topics. There is only one generated book title! Don't give any explanation or add any symbols, just write the title of the book. The requirement for this title is that it must be between 7 and 25 words long, and it must be attractive enough!",
            },
            {
                "role": "user",
                "content": f"Generate a book title for the following topic. There is only one generated book title! Don't give any explanation or add any symbols, just write the title of the book. The requirement for this title is that it must be at least 7 words and 25 words long, and it must be attractive enough:\n\n{prompt}",
            },
        ],
        temperature=0.7,
        max_tokens=100,
        top_p=1,
        stream=False,
        stop=None,
    )

    return completion.choices[0].message.content.strip()


def generate_book_structure(
    prompt: str,
    additional_instructions: str,
    seed_content: str,
    writing_style: str,
    complexity_level: str,
):
    """
    Returns book structure content as well as total tokens and total time for generation.
    """
    completion = st.session_state.groq.chat.completions.create(
        model="llama3-70b-8192",
        messages=[
            {
                "role": "system",
                # "content": 'Write in JSON format:\n\n{"Title of section goes here":"Description of section goes here",\n"Title of section goes here":{"Title of section goes here":"Description of section goes here","Title of section goes here":"Description of section goes here","Title of section goes here":"Description of section goes here"}}',
                "content": f'Create a book structure using the following parameters:\nWriting Style: {writing_style}\nComplexity Level: {complexity_level}\n\n. Write in JSON format:\n\n{{"Title of section goes here":"Description of section goes here","Title of section goes here":{{"Title of section goes here":"Description of section goes here","Title of section goes here":"Description of section goes here","Title of section goes here":"Description of section goes here"}}}}',
            },
            {
                "role": "user",
                # "content": f"Write a comprehensive structure, omiting introduction and conclusion sections (forward, author's note, summary), for a long (>300 page) book. It is very important that use the following subject and additional instructions to write the book. \n\n<subject>{prompt}</subject>\n\n<additional_instructions>{additional_instructions}</additional_instructions>",
                "content": f"Write a comprehensive structure, omitting introduction and conclusion sections (foreword, author's note, summary), for a book. Use the following subject and additional instructions to write the book. If seed content is provided, incorporate it into the structure.\n\n<subject>{prompt}</subject>\n\n<additional_instructions>{additional_instructions}</additional_instructions>\n\n<seed_content>{seed_content}</seed_content>",
            },
        ],
        temperature=0.3,
        max_tokens=8000,
        top_p=1,
        stream=False,
        response_format={"type": "json_object"},
        stop=None,
    )

    usage = completion.usage
    statistics_to_return = GenerationStatistics(
        input_time=usage.prompt_time,
        output_time=usage.completion_time,
        input_tokens=usage.prompt_tokens,
        output_tokens=usage.completion_tokens,
        total_time=usage.total_time,
        model_name="llama3-70b-8192",
    )

    return statistics_to_return, completion.choices[0].message.content


def generate_section(
    prompt: str,
    additional_instructions: str,
    seed_content: str,
    writing_style: str,
    complexity_level: str,
):
    stream = st.session_state.groq.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {
                "role": "system",
                "content": "You are an expert writer creating a comprehensive book chapter. Your writing should be: - \n\nEngaging and tailored to the specified writing style, tone, and complexity level. \nWell-structured with clear subheadings, paragraphs, and transitions. \nRich in relevant examples, analogies, and explanations. \nConsistent with provided seed content and additional instructions. \nFocused on delivering value through insightful analysis and information. \nFactually accurate based on the latest available information. \nCreative, offering unique perspectives or thought-provoking ideas. \n\nEnsure each section flows logically, maintaining coherence throughout the chapter",
            },
            {
                "role": "user",
                "content": f"Generate a long, comprehensive, structured chapter. Use the following section and important instructions:\n\n<section_title>{prompt}</section_title>\n\n<additional_instructions>{additional_instructions}</additional_instructions>\n\n<seed_content>{seed_content}</seed_content>\n\n<writing_style>{writing_style}</writing_style>\n\n<complexity_level>{complexity_level}</complexity_level> \n\n Please incorporate the following elements in your chapter: \n1. An engaging introduction that sets the context for the section. \n2. Clear and logical subheadings to organize the content. \n3. In-depth explanations of key concepts, with examples where appropriate. \n4. Critical analysis or discussion of the topic's importance or implications. \n5. A novel perspective or thought-provoking idea related to the topic. \n6. A conclusion that summarizes the main points and potentially links to the next section",
            },
        ],
        temperature=0.3,
        max_tokens=8000,
        top_p=1,
        stream=True,
        stop=None,
    )

    for chunk in stream:
        tokens = chunk.choices[0].delta.content
        if tokens:
            yield tokens
        if x_groq := chunk.x_groq:
            if not x_groq.usage:
                continue
            usage = x_groq.usage
            statistics_to_return = GenerationStatistics(
                input_time=usage.prompt_time,
                output_time=usage.completion_time,
                input_tokens=usage.prompt_tokens,
                output_tokens=usage.completion_tokens,
                total_time=usage.total_time,
                model_name="llama3-8b-8192",
            )
            yield statistics_to_return


def disable():
    st.session_state.button_disabled = True


def enable():
    st.session_state.button_disabled = False


def empty_st():
    st.empty()


def process_uploaded_file(uploaded_file):
    if uploaded_file is not None:
        return uploaded_file.getvalue().decode("utf-8")
    return ""


# Get the current active tab from URL parameters
active_tab = st.query_params.get("tab", "Generate Book")

# Create tabs
tab_names = ["Generate Book", "Generation Statistics", "About"]
tabs = st.tabs(tab_names)

# Set the active tab
active_tab_index = tab_names.index(active_tab)


def switch_to_tab(tab_name):
    st.query_params["tab"] = tab_name


with tabs[0]:
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
                    file_name=f"{st.session_state.book_title}.txt",
                    mime="text/plain",
                )

                # Create pdf file (styled)
                pdf_file = create_pdf_file(st.session_state.book.get_markdown_content())
                st.download_button(
                    label="Download PDF",
                    data=pdf_file,
                    file_name=f"{st.session_state.book_title}.pdf",
                    mime="application/pdf",
                )
            else:
                raise ValueError(
                    "Please generate content first before downloading th book.    "
                )


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

            seed_content = st.text_area(
                "Seed Content (optional)",
                help="Provide any existing notes or content to be incorporated into the     book",
                placeholder="Enter your existing notes or content here...",
                height=200,
                value="",
            )

            uploaded_file = st.file_uploader(
                "Or upload a text file",
                type=["txt"],
                help="Upload a text file with your seed content (optional)",
            )

            # Advanced options (you can move this to a sidebar if preferred)
            st.subheader("Advanced Options")
            writing_style = st.selectbox(
                "Writing Style", ["Casual", "Formal", "Academic", "Creative"]
            )
            complexity_level = st.select_slider(
                "Complexity Level",
                options=["Beginner", "Intermediate", "Advanced", "Expert"],
            )
            additional_instructions = st.text_area(
                "Additional Instructions (optional)",
                help="Provide any specific guidelines or preferences for the book's content",
                placeholder="E.g., 'Focus on beginner-friendly content', 'Include case studies', etc.",
            )

            # Generate button
            submitted = st.form_submit_button(
                st.session_state.button_text,
                on_click=disable,
                disabled=st.session_state.button_disabled,
            )

            if submitted:
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

                with st.spinner("Generating book"):
                    if len(topic_text) < 10:
                        raise ValueError(
                            "Book topic must be at least 10 characters long"
                        )

                    st.session_state.button_disabled = True
                    st.session_state.statistics_text = (
                        "Generating book title and structure in  background...."
                    )

                    if uploaded_file:
                        seed_content += "\n" + process_uploaded_file(uploaded_file)

                    display_statistics()

                    if not GROQ_API_KEY:
                        st.session_state.groq = Groq(api_key=groq_input_key)

                    large_model_generation_statistics, book_structure = (
                        generate_book_structure(
                            topic_text,
                            additional_instructions,
                            seed_content,
                            writing_style,
                            complexity_level,
                        )
                    )
                    # Generate AI book title
                    st.session_state.book_title = generate_book_title(topic_text)
                    st.write(f"## {st.session_state.book_title}")

                    with st.spinner("Generating book structure..."):
                        large_model_generation_statistics, book_structure = (
                            generate_book_structure(
                                topic_text,
                                additional_instructions,
                                seed_content,
                                writing_style,
                                complexity_level,
                            )
                        )

                    total_generation_statistics = GenerationStatistics(
                        model_name="llama3-8b-8192"
                    )

                    try:
                        book_structure_json = json.loads(book_structure)
                        book = Book(st.session_state.book_title, book_structure_json)

                        if "book" not in st.session_state:
                            st.session_state.book = book

                        # Print the book structure to the terminal to show structure
                        print("line 514")
                        print(json.dumps(book_structure_json, indent=2))

                        st.session_state.book.display_structure()

                        def stream_section_content(sections):
                            for title, content in sections.items():
                                if isinstance(content, str):
                                    content_stream = generate_section(
                                        title + ": " + content,
                                        additional_instructions,
                                        seed_content,
                                        writing_style,
                                        complexity_level,
                                    )
                                    for chunk in content_stream:
                                        # Check if GenerationStatistics data is returned instead    of str tokens
                                        chunk_data = chunk
                                        if type(chunk_data) == GenerationStatistics:
                                            total_generation_statistics.add(chunk_data)

                                            st.session_state.statistics_text = str(
                                                total_generation_statistics
                                            )
                                            display_statistics()

                                        elif chunk != None:
                                            st.session_state.book.update_content(
                                                title, chunk
                                            )
                                elif isinstance(content, dict):
                                    stream_section_content(content)

                        with st.spinner("Generating book content..."):
                            stream_section_content(book_structure_json)

                        st.success("Book generation complete!")

                    except json.JSONDecodeError:
                        st.error(
                            "Failed to decode the book structure. Please try again."
                        )

                    enable()

        
    except Exception as e:
        st.session_state.button_disabled = False
        st.error(e)

        if st.button("Clear"):
            st.rerun()

with tabs[1]:
    st.header("Generation Statistics")
    if "statistics_text" in st.session_state:
        st.write(st.session_state.statistics_text)
    else:
        st.info(
            "No generation statistics available. Generate a book to see statistics."
        )

with tabs[2]:
    st.header("About GroqBook")
    st.write(
        """
    GroqBook is an AI-powered book generation tool that uses the llama3 model (8b and 70b versions) on the Groq platform.
    It allows users to input a topic, provide seed content, and customize various aspects of the book generation process.
    
    Key Features:
    - Generates full book structures and content
    - Customizable writing style and complexity level
    - Ability to input seed content and additional instructions
    - Provides generation statistics for transparency
    
    This tool is designed for educational and creative purposes. The generated content should be reviewed and edited by human authors.
    """
    )
