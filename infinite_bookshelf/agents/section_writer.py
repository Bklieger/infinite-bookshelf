"""
Agent to generate book section content
"""

from ..inference import GenerationStatistics
import requests
import json

def generate_section(
    prompt: str, additional_instructions: str, model: str, headers
):
    url = "https://free.v36.cm/v1/chat/completions"
    
    data = {
        "model": "gpt-4o-mini",
        "messages": [
            {
                "role": "system",
                "content": """You are an expert writer specializing in creating engaging, well-researched book content. Your task is to generate a comprehensive chapter that is:
1. Well-structured with clear paragraphs and smooth transitions
2. Rich in detail and examples
3. Written in an engaging, professional style
4. Consistent in tone and terminology
5. Factually accurate and well-researched

Follow any additional instructions precisely as they represent specific requirements from the author.""",
            },
            {
                "role": "user",
                "content": f"""Generate a detailed, engaging chapter that thoroughly explores the topic. Please ensure:
- Comprehensive coverage of all key aspects
- Clear structure with logical flow
- Engaging examples and explanations
- Professional writing style

Section to write about:
<section_title>{prompt}</section_title>

Important instructions to follow:
<additional_instructions>{additional_instructions}</additional_instructions>""",
            },
        ],
        "temperature": 0.3,
        "max_tokens": 8000,
        "top_p": 1,
        "stream": True,
        "stop": None,
    }

    response = requests.post(url, json=data, headers=headers, stream=True)
    
    for line in response.iter_lines():
        if line:
            # Skip empty lines
            line = line.decode('utf-8')
            if line.startswith('data: '):
                line = line[6:]  # Remove 'data: ' prefix
                if line.strip() == '[DONE]':
                    break
                try:
                    chunk = json.loads(line)
                    tokens = chunk['choices'][0]['delta'].get('content', '')
                    if tokens:
                        yield tokens
                    if x_groq := chunk.get('x-groq'):
                        if not x_groq.get('usage'):
                            continue
                        usage = x_groq['usage']
                        statistics_to_return = GenerationStatistics(
                            input_time=usage['prompt_time'],
                            output_time=usage['completion_time'],
                            input_tokens=usage['prompt_tokens'],
                            output_tokens=usage['completion_tokens'],
                            total_time=usage['total_time'],
                            model_name=model,
                        )
                        yield statistics_to_return
                except json.JSONDecodeError:
                    continue
