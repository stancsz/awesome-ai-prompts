import json

def check_ids():
    with open("docs/prompts.json", "r") as f:
        prompts = json.load(f)

    missing = [i for i, p in enumerate(prompts) if 'id' not in p or not p['id']]
    if missing:
        print(f"Found {len(missing)} prompts without ID!")
    else:
        print("All prompts have IDs.")

if __name__ == "__main__":
    check_ids()
