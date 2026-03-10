Kharagpur Data Science Hackathon 2026
Track A: Long-Context Narrative Consistency Verification

--Overview--
This project addresses the Kharagpur Data Science Hackathon (KDSH) 2026 Track A problem:
verifying whether a hypothetical character backstory is causally and logically consistent
with a long-form literary narrative (novels exceeding 100k words).

Rather than treating the task as text generation or summarization, we formulate it as a
constraint-based reasoning problem grounded strictly in explicit textual evidence.

--------------------------------


Key Design Principles
• Treat the task as causal consistency verification, not creative generation.
• Decompose each backstory into atomic, verifiable factual claims.
• Search for evidence across the entire narrative, not local passages.
• Enforce an explicit-evidence-only rule (no inference or speculation).
• Prefer interpretability and conservative aggregation.
• Ensure end-to-end reproducibility.

--------------------------------

System Architecture
The pipeline follows a modular, interpretable design:

1. Claim Extraction
   Each backstory is decomposed into atomic factual claims using a lightweight
   transformer-based LLM with deterministic prompting.

2. Long-Context Handling
   Full novels are preprocessed into paragraph-aware chunks and stored as JSONL files.
   This avoids truncation and preserves narrative structure.

3. Evidence Retrieval
   Candidate passages are retrieved using character-aware lexical filtering,
   ensuring high precision while remaining computationally efficient.

4. Explicit Consistency Checking
   For each claim, the system checks whether the novel explicitly:
   • Supports the claim
   • Contradicts the claim
   • Does not mention the claim

5. Conservative Aggregation
   • Any explicit contradiction → inconsistent (0)
   • Any explicit support → consistent (1)
   • Otherwise → unsupported (0)

KDS_HACKATHON/
├── data/
│   ├── books/         # Full novel texts
│   ├── train.csv
│   └── test.csv
├── src/
│   ├── ingest.py      # Data loading and preprocessing
│   ├── chunk.py       # Paragraph-aware chunking
│   ├── indexer.py     # Embeddings + temporal metadata
│   ├── reason.py      # Claim reasoning and NLI verification
│   └── predict.py     # End-to-end pipeline
├── results.csv        # Generated predictions
├── requirements.txt
├── Squad 404_Report.pdf
└── README.md
```

--Environment & Setup--

--Tested with:
• Python 3.11
• Ubuntu 22.04 (also compatible with Windows, macOS, WSL)

--Install dependencies:
 
 -pip install -r requirements.txt

-Set API key (example for Linux/macOS):
-export GROQ_API_KEY=your_key_here

--------------------------------

--Running the Pipeline
-From the project root directory:
 python scripts/run_pipeline.py

--This command:
• Reads the provided test CSV
• Processes full novels without truncation
• Extracts and verifies claims
• Generates results.csv automatically

--------------------------------

--Output Format--
--The system produces a single file:
  results.csv

--Format:
Story ID, Prediction, Rationale

--Prediction:
1 → Backstory is explicitly supported by the novel
0 → Backstory is contradicted or unsupported

--------------------------------

--Modeling Choices--
--This project uses:
• Transformer-based LLMs for claim extraction and verification
• A symbolic, rule-based aggregation layer
• Hybrid neural-symbolic reasoning (LLM + deterministic logic)

-No black-box end-to-end prompting is used.

--------------------------------

--Handling Noise and Hallucination--
• Claims not explicitly mentioned are rejected
• Narrative plausibility is ignored
• Only verbatim or near-verbatim textual evidence is accepted

--------------------------------

--Limitations--
• Implicit or thematic consistency is not captured
• Characters with sparse mentions may yield unsupported results
• Conservative bias favors precision over recall

--------------------------------

--Reproducibility--
• Fully automated pipeline
• Deterministic outputs given identical inputs
• No manual intervention required
• Clean-environment compatible

--------------------------------

--Track Declaration--
-Track: A — Systems Reasoning with NLP and Generative AI

--------------------------------

--Authors
-Team submission for Kharagpur Data Science Hackathon 2026.

