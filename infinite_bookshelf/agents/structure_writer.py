"""
Agent to generate book structure
"""

from ..inference import GenerationStatistics
from ..prompts import (
    STRUCTURE_WRITER_LONG_PROMPT, 
    STRUCTURE_WRITER_SHORT_PROMPT,
    ADVANCED_STRUCTURE_WRITER_LONG_PROMPT,
    ADVANCED_STRUCTURE_WRITER_SHORT_PROMPT
)


def generate_book_structure(
    prompt: str,
    additional_instructions: str,
    model: str,
    groq_provider,
    long: bool = False,
    advanced: bool = False
):
    """
    Returns book structure content as well as total tokens and total time for generation.
    """

    if advanced:
        USER_PROMPT = ADVANCED_STRUCTURE_WRITER_LONG_PROMPT if long else ADVANCED_STRUCTURE_WRITER_SHORT_PROMPT
    else:
        USER_PROMPT = STRUCTURE_WRITER_LONG_PROMPT if long else STRUCTURE_WRITER_SHORT_PROMPT

    USER_PROMPT = USER_PROMPT.format(prompt=prompt, additional_instructions=additional_instructions)

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
