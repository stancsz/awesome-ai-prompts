import csv
import json
import os
import hashlib

def generate_id(text):
    return hashlib.md5(text.encode('utf-8')).hexdigest()

def main():
    repo_root = os.getcwd()
    prompts = []

    # Walk through all directories
    for root, dirs, files in os.walk(repo_root):
        if "prompts.csv" in files:
            category = os.path.basename(root)
            # Skip if category is the repo root itself (unlikely but possible)
            if root == repo_root:
                continue

            csv_path = os.path.join(root, "prompts.csv")
            print(f"Processing {category}...")

            try:
                with open(csv_path, 'r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        if not row.get('prompt'):
                            continue

                        prompt_text = row['prompt']
                        prompt_id = generate_id(prompt_text)

                        prompt_data = {
                            "id": prompt_id,
                            "category": category,
                            "prompt": prompt_text,
                            "contributor": row.get('contributor', ''),
                            "comment": row.get('comment', '')
                        }
                        prompts.append(prompt_data)
            except Exception as e:
                print(f"Error processing {csv_path}: {e}")

    # Write to docs/prompts.json
    output_path = os.path.join(repo_root, "docs", "prompts.json")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(prompts, f, indent=2, ensure_ascii=False)

    print(f"Successfully generated {len(prompts)} prompts in {output_path}")

if __name__ == "__main__":
    main()
