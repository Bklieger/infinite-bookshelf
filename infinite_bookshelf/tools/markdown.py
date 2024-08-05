"""
Functions to manage markdown content
"""

from io import BytesIO


def create_markdown_file(content: str) -> BytesIO:
    """
    Create a Markdown file from the provided content.
    """
    markdown_file = BytesIO()
    markdown_file.write(content.encode("utf-8"))
    markdown_file.seek(0)
    return markdown_file
