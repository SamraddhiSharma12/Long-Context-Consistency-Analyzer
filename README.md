# Kharagpur Data Science Hackathon 2026 — Track A Submission

**Team Name:** Squad 404  
**Track:** A — Systems Reasoning with NLP and Generative AI

---

## Overview
This repository contains our submission for the **Kharagpur Data Science Hackathon 2026 (Track A)**.

The task is to verify whether a proposed character backstory is **consistent (1)** or **inconsistent (0)** with a full-length novel. The focus is on long-context reasoning, evidence aggregation, and causal consistency rather than text generation or summarization.

---

## Repository Structure
```
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

---

## Environment
- **Tested on:** Ubuntu 22.04 (WSL2)
- **Python:** 3.11 / 3.12
- The project is OS-agnostic and should run on Linux, macOS, or Windows.

---

## Running the Project (Judge / Clean Environment Instructions)

The following steps describe how to run the project from a **fresh environment**, exactly as intended for evaluation.

### 1. Ensure Python and venv support are installed
On Ubuntu / Debian systems:
```bash
sudo apt update
sudo apt install python3 python3-venv
```

---

### 2. Create and activate a virtual environment
From the project root directory:
```bash
python3 -m venv venv_test
source venv_test/bin/activate
```

You should now see `(venv_test)` in your terminal prompt.

---

### 3. Install dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

This will install all required libraries, including Pathway, PyTorch, and Transformers.

---

### 4. Run the prediction pipeline
```bash
# Set your API Key (Example for Groq)
export GROQ_API_KEY=your_key_here

# Run the end-to-end pipeline
python scripts/run_pipeline.py
python -m src.predict
```

The pipeline will:
1. Load full novels and metadata
2. Build embeddings and temporal chunk metadata
3. Perform claim-based reasoning with NLI verification
4. Generate `results.csv`

Successful execution ends with:
```
Saved results.csv with 60 rows
```

---

## Output Format
The generated `results.csv` follows the format specified in the problem statement:

```csv
id,prediction,rationale
```

- `prediction = 1` → backstory is consistent
- `prediction = 0` → backstory is inconsistent
- `rationale` provides a short explanation (optional but encouraged)

---

## Reproducibility Notes
- No preprocessed data, caches, or embeddings are included
- All intermediate artifacts are generated at runtime
- No paid or external APIs are used
- GPU acceleration is used automatically if available, otherwise CPU is used

This design ensures clean, reproducible execution in a fresh environment.

---

## Track Declaration
**Track:** A — Systems Reasoning with NLP and Generative AI

---

## Team
**Squad 404**

---

## Notes for Evaluators
This system is intentionally conservative. In the absence of strong supporting evidence, it defaults to inconsistency. This behavior is aligned with the goal of verifying narrative coherence rather than maximizing positive predictions.

