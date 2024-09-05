"""
Agent to generate book structure
"""

from ..inference import GenerationStatistics


def generate_book_structure(
    prompt: str,
    additional_instructions: str,
    model: str,
    groq_provider,
    long: bool = False,
):
    """
    Returns book structure content as well as total tokens and total time for generation.
    """

    if long:
        USER_PROMPT = f"""Craft a comprehensive and detailed structure for an extensive book (300+ pages), excluding introductory and concluding sections. Ensure each chapter and subsection is distinct, with clear titles and descriptions that avoid overlap. Adhere strictly to the following subject matter and additional guidelines:

<subject>{prompt}</subject>

<additional_instructions>{additional_instructions}</additional_instructions>"""
    else:
        USER_PROMPT = f"""Design a well-structured outline for a book, providing only one level of depth for nested sections. Create distinct chapters with clear, non-overlapping titles and descriptions. Omit introductory and concluding sections. Adhere strictly to the following subject matter and additional guidelines:

<subject>{prompt}</subject>

<additional_instructions>{additional_instructions}</additional_instructions>"""

    completion = groq_provider.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": 'Write in JSON format:\n\n{"Title of section goes here":"Description of section goes here",\n"Title of section goes here":{"Title of section goes here":"Description of section goes here","Title of section goes here":"Description of section goes here","Title of section goes here":"Description of section goes here"}}',
            },
            {
                "role": "user",
                "content": USER_PROMPT,
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
        model_name=model,
    )

    return statistics_to_return, completion.choices[0].message.content
