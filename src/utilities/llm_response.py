import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_answer(query: str, contexts: list[str], model="gpt-3.5-turbo") -> str:
    context_text = "\n\n".join(contexts)
    prompt = f"""
You are an AI assistant helping students write internship reports.

Context:
{context_text}

Question:
{query}

Answer:
"""

    response = openai.ChatCompletion.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are an expert in analyzing internship reports."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3,
        max_tokens=500
    )

    return response['choices'][0]['message']['content']
