import os
import subprocess

BOOKS_DIR = "data/books"
DATA_DIR = "data"

def process_book(book_file):
    book_name = book_file.replace(".txt", "")
    print(f"\n📘 Processing book: {book_name}")

    raw_path = os.path.join(BOOKS_DIR, book_file)
    clean_path = os.path.join(DATA_DIR, f"{book_name}_clean.txt")
    chunk_path = os.path.join(DATA_DIR, f"{book_name}_chunks.jsonl")

    # Step 1: Clean
    subprocess.run([
        "python", "scripts/clean.py",
        raw_path,
        clean_path
    ], check=True)

    # Step 2: Chunk
    subprocess.run([
        "python", "scripts/chunk.py",
        clean_path,
        chunk_path
    ], check=True)

    print(f"✅ Finished: {book_name}")

def main():
    books = [f for f in os.listdir(BOOKS_DIR) if f.endswith(".txt")]

    if not books:
        print("❌ No books found in data/books/")
        return

    for book in books:
        process_book(book)

if __name__ == "__main__":
    main()
