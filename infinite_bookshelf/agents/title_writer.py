"""
Agent to generate book title
"""

from ..inference import GenerationStatistics
from ..prompts import (
    TITLE_WRITER_SYSTEM_PROMPT, 
    TITLE_WRITER_USER_PROMPT,
    ADVANCED_TITLE_WRITER_SYSTEM_PROMPT,
    ADVANCED_TITLE_WRITER_USER_PROMPT
)


def generate_book_title(prompt: str, model: str, groq_provider, advanced: bool = False):
    """
    Generate a book title using AI.
    """
    system_prompt = ADVANCED_TITLE_WRITER_SYSTEM_PROMPT if advanced else TITLE_WRITER_SYSTEM_PROMPT
    user_prompt = ADVANCED_TITLE_WRITER_USER_PROMPT if advanced else TITLE_WRITER_USER_PROMPT

    completion = groq_provider.chat.completions.create(
        model="llama3-70b-8192",
        messages=[
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": user_prompt.format(prompt=prompt),
            },
        ],
        temperature=0.7,
        max_tokens=100,
        top_p=1,
        stream=False,
        stop=None,
    )

    return completion.choices[0].message.content.strip()
