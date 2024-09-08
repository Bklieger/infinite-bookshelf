"""
Agent to generate book section content
"""

from ..inference import GenerationStatistics
from ..prompts import (
    SECTION_WRITER_SYSTEM_PROMPT, 
    SECTION_WRITER_USER_PROMPT,
    ADVANCED_SECTION_WRITER_SYSTEM_PROMPT,
    ADVANCED_SECTION_WRITER_USER_PROMPT
)


def generate_section(
    prompt: str, 
    additional_instructions: str, 
    model: str, 
    groq_provider,
    advanced: bool = False
):
    system_prompt = ADVANCED_SECTION_WRITER_SYSTEM_PROMPT if advanced else SECTION_WRITER_SYSTEM_PROMPT
    user_prompt = ADVANCED_SECTION_WRITER_USER_PROMPT if advanced else SECTION_WRITER_USER_PROMPT

    stream = groq_provider.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": user_prompt.format(prompt=prompt, additional_instructions=additional_instructions),
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
                model_name=model,
            )
            yield statistics_to_return
