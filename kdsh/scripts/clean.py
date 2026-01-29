import sys
from pathlib import Path
import re

def clean_text(text: str) -> str:
    # Remove Project Gutenberg headers
    text = re.sub(r"\*{3}.*?\*{3}", "", text, flags=re.DOTALL)

    # Normalize spaces
    text = re.sub(r"\s+", " ", text)

    return text.strip()

def main():
    if len(sys.argv) != 3:
        print("Usage: python clean.py <input_txt> <output_txt>")
        sys.exit(1)

    input_path = Path(sys.argv[1])
    output_path = Path(sys.argv[2])

    text = input_path.read_text(encoding="utf-8", errors="ignore")
    cleaned = clean_text(text)

    output_path.write_text(cleaned, encoding="utf-8")

    print(f"🧹 Cleaned: {input_path.name}")

if __name__ == "__main__":
    main()
