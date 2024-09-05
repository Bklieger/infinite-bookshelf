"""
Agent to generate book section content
"""

from ..inference import GenerationStatistics


def generate_section(
    prompt: str, additional_instructions: str, model: str, groq_provider
):
    stream = groq_provider.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": "As an expert writer, generate a comprehensive, well-structured, and in-depth chapter for the given section. Pay close attention to any additional instructions provided, as they are crucial to the content's direction and quality. Focus solely on producing the content without any extraneous commentary."
            },
            {
                "role": "user",
                "content": f"""Craft a detailed, well-organized, and extensive chapter based on the following section title and important guidelines:

<section_title>{prompt}</section_title>

<additional_instructions>{additional_instructions}</additional_instructions>

Ensure the content is thorough, engaging, and adheres closely to the provided instructions."""
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
