import csv
from decide_consistency import decide


def main():
    print("\n🚀 Starting pipeline for TEST split only", flush=True)

    input_csv = "data/csv/test.csv"
    output_csv = "results.csv"

    results = []

    with open(input_csv, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        for idx, row in enumerate(reader, start=1):
            print(f"➡️ Processing row {idx} (Story ID={row['id']})", flush=True)

            story_id = row["id"]
            book = row["book_name"]
            character = row["char"]
            backstory = row["content"]

            prediction, rationale = decide(book, character, backstory)

            results.append({
                "Story ID": story_id,
                "Prediction": prediction,
                "Rationale": rationale
            })

    with open(output_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["Story ID", "Prediction", "Rationale"]
        )
        writer.writeheader()
        writer.writerows(results)

    print(f"✅ Finished TEST split → {output_csv}", flush=True)


if __name__ == "__main__":
    print("🔥 run_pipeline.py started", flush=True)
    main()
    print("🏁 Pipeline completed", flush=True)
