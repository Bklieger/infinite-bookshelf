ADVANCED_SECTION_WRITER_SYSTEM_PROMPT = """As an expert writer, generate a comprehensive, well-structured, and in-depth chapter for the given section. Pay close attention to any additional instructions provided, as they are crucial to the content's direction and quality. Focus solely on producing the content without any extraneous commentary.

Craft comprehensive book chapters that are:
    1. Captivating and precisely aligned with the specified writing style, tone, and complexity level.
    2. Meticulously structured with clear, hierarchical subheadings, well-defined paragraphs, and smooth transitions.
    3. Abundant in pertinent examples, vivid analogies, and lucid explanations to enhance understanding.
    4. Seamlessly integrated with provided seed content and additional instructions.
    5. Laser-focused on delivering exceptional value through penetrating analysis and actionable information.
    6. Rigorously fact-checked and updated with the most current, authoritative information available.
    7. Imaginative, presenting fresh perspectives and intellectually stimulating ideas.
    8. Logically coherent, ensuring a smooth flow of ideas within each section and maintaining narrative consistency throughout the chapter.
    9. Engaging the reader's curiosity and encouraging critical thinking.
    10. Tailored to the target audience's needs and expectations."""

ADVANCED_SECTION_WRITER_USER_PROMPT = """Craft comprehensive book chapters that are:
    1. Captivating and precisely aligned with the specified writing style, tone, and complexity level.
    2. Meticulously structured with clear, hierarchical subheadings, well-defined paragraphs, and smooth transitions.
    3. Abundant in pertinent examples, vivid analogies, and lucid explanations to enhance understanding.
    4. Seamlessly integrated with provided seed content and additional instructions.
    5. Laser-focused on delivering exceptional value through penetrating analysis and actionable information.
    6. Rigorously fact-checked and updated with the most current, authoritative information available.
    7. Imaginative, presenting fresh perspectives and intellectually stimulating ideas.
    8. Logically coherent, ensuring a smooth flow of ideas within each section and maintaining narrative consistency throughout the chapter.
    9. Engaging the reader's curiosity and encouraging critical thinking.
    10. Tailored to the target audience's needs and expectations.

Use the following section and important instructions:

<section_title>{prompt}</section_title>

<additional_instructions>{additional_instructions}</additional_instructions>

Adhere strictly to these crucial parameters:
    1. Writing Style: {writing_style} - Maintain this style consistently throughout the text.
    2. Complexity Level: {complexity_level} - Ensure all content aligns with this specified level of complexity.
    3. Audience Engagement: Craft the content to resonate deeply with the intended readership.
    4. Coherence: Maintain a unified voice and consistent argumentation across all chapters.
    5. Originality: Strive for unique insights and novel approaches within the chosen topic."""

ADVANCED_STRUCTURE_WRITER_LONG_PROMPT = """Craft a comprehensive and detailed structure for an extensive book (300+ pages), excluding introductory and concluding sections. Ensure each chapter and subsection is distinct, with clear titles and descriptions that avoid overlap. Adhere strictly to the following subject matter and additional guidelines:
<subject>{prompt}</subject>
<additional_instructions>{additional_instructions}</additional_instructions>"""

ADVANCED_STRUCTURE_WRITER_SHORT_PROMPT = """Design a well-structured outline for a book, providing only one level of depth for nested sections. Create distinct chapters with clear, non-overlapping titles and descriptions. Omit introductory and concluding sections. Adhere strictly to the following subject matter and additional guidelines:
<subject>{prompt}</subject>
<additional_instructions>{additional_instructions}</additional_instructions>"""

ADVANCED_TITLE_WRITER_SYSTEM_PROMPT = """Generate a single, captivating book title for the provided topic. The title should be between 7 and 25 words long, engaging, and relevant. Provide only the title without any additional explanation or symbols."""

ADVANCED_TITLE_WRITER_USER_PROMPT = """Create an enticing book title for the following topic. Remember, provide only one title without any explanation or symbols. The title must be between 7 and 25 words long and should be compelling:

{prompt}"""