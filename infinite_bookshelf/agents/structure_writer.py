"""
Agent to generate book structure
"""

from ..inference import GenerationStatistics
import requests

def generate_book_structure(
    prompt: str,
    additional_instructions: str,
    model: str,
    headers,
    long: bool = False,
):
    """
    Returns book structure content as well as total tokens and total time for generation.
    """

    if long:
        USER_PROMPT = f"""Design a comprehensive book structure for an in-depth (300+ pages) exploration of the subject. Requirements:
- Create compelling, SEO-friendly chapter titles that capture the essence of each section
- Ensure a natural progression of topics, from foundational concepts to advanced applications
- Include practical examples, case studies, or exercises where relevant
- Balance theoretical knowledge with real-world applications
- Incorporate industry best practices and current trends
- Consider both beginner and advanced reader needs

Subject to write about:
<subject>{prompt}</subject>

Important guidelines to follow:
<additional_instructions>{additional_instructions}</additional_instructions>"""
    else:
        USER_PROMPT = f"""Design a focused book structure that delivers maximum value. Requirements:
- Create engaging, keyword-rich chapter titles
- Structure content from basic to advanced concepts
- Include practical applications and examples
- Ensure each section provides actionable insights
- Maintain clear progression and logical flow
- Focus on essential concepts and key takeaways

Subject to write about:
<subject>{prompt}</subject>

Important guidelines to follow:
<additional_instructions>{additional_instructions}</additional_instructions>"""

    url = "https://free.v36.cm/v1/chat/completions"
    
    data = {
        "model": "gpt-4o-mini",
        "messages": [
            {
                "role": "system",
                "content": """You are an expert book architect specializing in creating engaging, market-ready book outlines. Output must be in this JSON format:

{
    "Chapter Title": "Clear description of chapter content and purpose",
    "Another Chapter": {
        "Subsection Title": "Description of subsection content",
        "Another Subsection": "Description of content"
    }
}

Guidelines:
1. Create SEO-optimized, compelling titles
2. Ensure smooth topic progression from basics to advanced
3. Balance theory with practical applications
4. Include examples, case studies, or exercises
5. Consider reader engagement and learning outcomes
6. Maintain consistent depth and detail level
7. Address both beginner and advanced needs""",
            },
            {
                "role": "user",
                "content": USER_PROMPT,
            },
        ],
        "temperature": 0.3,
        "max_tokens": 8000,
        "top_p": 1,
        "stream": False,
        "response_format": {"type": "json_object"},
        "stop": None,
    }

    response = requests.post(url, json=data, headers=headers)
    completion = response.json()

    usage = completion['usage']
    statistics_to_return = GenerationStatistics(
        input_time=usage['prompt_time'],
        output_time=usage['completion_time'],
        input_tokens=usage['prompt_tokens'],
        output_tokens=usage['completion_tokens'],
        total_time=usage['total_time'],
        model_name="gpt-4o-mini",
    )

    return statistics_to_return, completion['choices'][0]['message']['content']
