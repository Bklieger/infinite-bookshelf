"""
Agent to generate book title
"""

import requests
from ..inference import GenerationStatistics


def generate_book_title(prompt: str, model: str, headers):
    """
    Generate a book title using AI.
    """
    url = "https://free.v36.cm/v1/chat/completions"
    
    data = {
        "model": "gpt-4o-mini",
        "messages": [
            {
                "role": "system",
                "content": """You are an expert in crafting bestselling book titles that drive sales and engagement. Your titles should be:
1. Attention-grabbing and memorable
2. SEO-optimized with relevant keywords
3. Between 7-25 words, with a strong main title and optional subtitle
4. Market-tested formats (e.g., "The Ultimate Guide to...", "Mastering...", "X Secrets of...")
5. Clear value proposition for the reader
6. Emotionally resonant and curiosity-inducing
7. Professional and authoritative

Output only the title - no explanations or additional text.""",
            },
            {
                "role": "user",
                "content": f"""Create a compelling, marketable book title that:
- Uses proven title patterns that drive sales
- Incorporates relevant keywords for SEO
- Promises clear value or benefits
- Creates curiosity or emotional connection
- Maintains professional authority
- Includes an optional subtitle for clarity
- Is between 7-25 words total

Topic to create title for:
{prompt}""",
            },
        ],
        "temperature": 0.7,
        "max_tokens": 100,
        "top_p": 1,
        "stream": False,
        "stop": None,
    }

    response = requests.post(url, json=data, headers=headers)
    completion = response.json()

    return completion['choices'][0]['message']['content'].strip()
