import json
import os
from groq import Groq
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

SYSTEM_PROMPT = """
You are an expert literary analyst.

Given a character backstory, extract atomic factual claims.

Rules:
- One claim = one explicit fact stated in the backstory
- Do NOT infer causes or motivations
- Even if context is incomplete, extract the stated fact
- Keep claims short and precise

Return ONLY a JSON list of strings.
"""

def extract_claims(backstory: str):
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": backstory}
        ],
        temperature=0
    )

    text = response.choices[0].message.content.strip()

    try:
        return json.loads(text)
    except Exception:
        # Fallback if model slightly breaks JSON
        return [
            line.strip("-• ")
            for line in text.splitlines()
            if line.strip()
        ]
