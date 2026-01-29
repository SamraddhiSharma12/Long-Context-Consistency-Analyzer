import json
import os
from pathlib import Path
from groq import Groq
from dotenv import load_dotenv

# -------------------------
# ENV SETUP
# -------------------------
load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# -------------------------
# HARD LIMITS (CRITICAL)
# -------------------------
MAX_CONTEXT_CHARS = 1500   # 🔒 Groq-safe
MAX_CHUNKS = 6             # scan more, send less

# -------------------------
# CACHE (STAND-OUT FEATURE)
# -------------------------
CACHE_PATH = Path("data/claim_evidence_cache.json")
CACHE = json.loads(CACHE_PATH.read_text(encoding="utf-8")) if CACHE_PATH.exists() else {}

# -------------------------
# SYSTEM PROMPT
# -------------------------
SYSTEM_PROMPT = """
You are a strict literary fact-checker.

Task:
Given a factual claim about a character and excerpts from a novel,
decide whether the novel:

- EXPLICITLY SUPPORTS the claim
- EXPLICITLY CONTRADICTS the claim
- DOES NOT MENTION the claim

Rules:
- Use ONLY explicit textual evidence
- Do NOT infer or speculate
- Quote exact text if possible

Return ONLY valid JSON:
{
  "verdict": "support | contradiction | unknown",
  "excerpt": "verbatim quote or empty string"
}
"""

# -------------------------
# MAIN FUNCTION
# -------------------------
def retrieve(book: str, character: str, claim: str):
    cache_key = f"{book}||{character}||{claim}"
    if cache_key in CACHE:
        return CACHE[cache_key]

    chunks_path = Path(f"data/{book}_chunks.jsonl")
    if not chunks_path.exists():
        return {"verdict": "unknown", "excerpt": ""}

    with chunks_path.open(encoding="utf-8") as f:
        chunks = [json.loads(line)["text"] for line in f]

    # -------------------------
    # CLAIM-AWARE FILTER (KEY FIX)
    # -------------------------
    claim_terms = [
        w.lower() for w in claim.split()
        if len(w) > 4
    ]

    candidates = []
    for text in chunks:
        t = text.lower()
        if character.lower() in t and any(term in t for term in claim_terms):
            candidates.append(text)
        if len(candidates) >= MAX_CHUNKS:
            break

    if not candidates:
        result = {"verdict": "unknown", "excerpt": ""}
        CACHE[cache_key] = result
        _save_cache()
        return result

    # -------------------------
    # STRICT CONTEXT BUDGET
    # -------------------------
    context = ""
    for c in candidates:
        if len(context) + len(c) > MAX_CONTEXT_CHARS:
            break
        context += "\n\n" + c

    # LAST SAFETY NET
    context = context[:MAX_CONTEXT_CHARS]

    # -------------------------
    # LLM CALL (SAFE)
    # -------------------------
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": f"""
CLAIM:
{claim}

NOVEL EXCERPTS:
{context}
"""
            }
        ],
        temperature=0
    )

    try:
        result = json.loads(response.choices[0].message.content)
    except Exception:
        result = {"verdict": "unknown", "excerpt": ""}

    CACHE[cache_key] = result
    _save_cache()
    return result

# -------------------------
# CACHE SAVE
# -------------------------
def _save_cache():
    CACHE_PATH.write_text(
        json.dumps(CACHE, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )
