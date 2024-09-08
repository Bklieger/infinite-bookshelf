SECTION_WRITER_SYSTEM_PROMPT = """You are an expert writer. Generate a long, comprehensive, structured chapter for the section provided. If additional instructions are provided, consider them very important. Only output the content."""

SECTION_WRITER_USER_PROMPT = """Generate a long, comprehensive, structured chapter. Use the following section and important instructions:

<section_title>{prompt}</section_title>

<additional_instructions>{additional_instructions}</additional_instructions>"""

STRUCTURE_WRITER_LONG_PROMPT = """Write a comprehensive structure, omiting introduction and conclusion sections (forward, author's note, summary), for a long (>300 page) book. It is very important that use the following subject and additional instructions to write the book.

<subject>{prompt}</subject>

<additional_instructions>{additional_instructions}</additional_instructions>"""

STRUCTURE_WRITER_SHORT_PROMPT = """Write a comprehensive structure, omiting introduction and conclusion sections (forward, author's note, summary), for a book. Only provide up to one level of depth for nested sections. Make clear titles and descriptions that have no overlap with other sections. It is very important that use the following subject and additional instructions to write the book.

<subject>{prompt}</subject>

<additional_instructions>{additional_instructions}</additional_instructions>"""

TITLE_WRITER_SYSTEM_PROMPT = """Generate suitable book titles for the provided topics. There is only one generated book title! Don't give any explanation or add any symbols, just write the title of the book. The requirement for this title is that it must be between 7 and 25 words long, and it must be attractive enough!"""

TITLE_WRITER_USER_PROMPT = """Generate a book title for the following topic. There is only one generated book title! Don't give any explanation or add any symbols, just write the title of the book. The requirement for this title is that it must be at least 7 words and 25 words long, and it must be attractive enough:

{prompt}"""