import os
import pandas as pd
from src.harvester import GutenbergHarvester

def main():
    os.makedirs("output", exist_ok=True)
    harvester = GutenbergHarvester(target_lang="es")
    
    # Target early 20th-century naturalist/realist authors and short forms
    queries = ["Quiroga", "Cuentos de la selva", "Fabulas"]
    all_records = []

    print("Fetching and screening candidates from Project Gutenberg...")
    for q in queries:
        books = harvester.search_candidates(q, limit=2)
        for book in books:
            gid = book.get("id")
            title = book.get("title", "Unknown Title")
            authors = ", ".join([a.get("name", "") for a in book.get("authors", [])]) or "Unknown Author"
            
            raw_text = harvester.download_text(book)
            if not raw_text:
                continue

            stories = harvester.split_into_stories(raw_text, title)
            for s_title, s_content in stories:
                row = harvester.score_text(gid, title, s_title, authors, s_content)
                all_records.append(row)

    df = pd.DataFrame(all_records)
    
    # Sort: Viable candidates first, then ranked by Readability and Dialogue
    df = df.sort_values(
        by=["viable", "fernandez_huerta", "dialogue_pct"], 
        ascending=[False, False, False]
    ).reset_index(drop=True)

    csv_path = os.path.join("output", "clinical_candidate_matrix.csv")
    df.to_csv(csv_path, index=False, encoding="utf-8-sig")

    print(f"\nMatrix successfully generated: {csv_path}")
    print("\n--- TOP SCREENED CANDIDATES ---")
    cols = ["viable", "story_title", "word_count", "fernandez_huerta", "dialogue_pct"]
    print(df[cols].head(5).to_string())

if __name__ == "__main__":
    main()
    