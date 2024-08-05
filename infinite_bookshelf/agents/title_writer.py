"""
Agent to generate book title
"""

from ..inference import GenerationStatistics


def generate_book_title(prompt: str, model: str, groq_provider):
    """
    Generate a book title using AI.
    """
    completion = groq_provider.chat.completions.create(
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
