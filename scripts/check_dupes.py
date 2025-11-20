import json
from collections import Counter

def check_duplicates():
    with open("docs/prompts.json", "r") as f:
        prompts = json.load(f)

    ids = [p['id'] for p in prompts]
    duplicates = [item for item, count in Counter(ids).items() if count > 1]

    if duplicates:
        print(f"Found {len(duplicates)} duplicate IDs!")
        for dup in duplicates[:5]:
            print(f"Duplicate ID: {dup}")
            # Find example prompts
            examples = [p for p in prompts if p['id'] == dup]
            print(f"  - {examples[0]['prompt'][:50]}...")
    else:
        print("No duplicate IDs found.")

if __name__ == "__main__":
    check_duplicates()
