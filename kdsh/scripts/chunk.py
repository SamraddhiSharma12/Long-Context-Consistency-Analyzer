import sys
import json

CHUNK_SIZE = 900

def main():
    if len(sys.argv) != 3:
        print("Usage: python chunk.py <clean_txt> <out_jsonl>")
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2]

    text = open(input_path, encoding="utf-8").read()
    words = text.split()

    chunks = []
    for i in range(0, len(words), CHUNK_SIZE):
        chunk_words = words[i:i+CHUNK_SIZE]
        chunks.append({
            "chunk_id": i // CHUNK_SIZE,
            "start_word": i,
            "end_word": min(i+CHUNK_SIZE, len(words)),
            "text": " ".join(chunk_words)
        })

    with open(output_path, "w", encoding="utf-8") as f:
        for c in chunks:
            f.write(json.dumps(c, ensure_ascii=False) + "\n")

    print(f"📦 Chunked: {output_path}")

if __name__ == "__main__":
    main()
