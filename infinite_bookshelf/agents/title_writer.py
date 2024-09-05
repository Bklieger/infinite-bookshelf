"""
Agent to generate book title
"""

from ..inference import GenerationStatistics


def generate_book_title(prompt: str, model: str, groq_provider):
    """
    Generate a book title using AI.
    """
    completion = groq_provider.chat.completions.create(
        model="llama-3.1-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": "Generate a single, captivating book title for the provided topic. The title should be between 7 and 25 words long, engaging, and relevant. Provide only the title without any additional explanation or symbols."
            },
            {
                "role": "user",
                "content": f"Create an enticing book title for the following topic. Remember, provide only one title without any explanation or symbols. The title must be between 7 and 25 words long and should be compelling:\n\n{prompt}"
            },
        ],
        temperature=0.7,
        max_tokens=100,
        top_p=1,
        stream=False,
        stop=None,
    )

    return completion.choices[0].message.content.strip()
