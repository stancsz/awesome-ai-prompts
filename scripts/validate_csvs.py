import csv
import os

def validate_csv(filepath):
    print(f"Validating {filepath}...")
    with open(filepath, 'r', encoding='utf-8') as f:
        # Read header
        header = f.readline().strip().split(',')
        print(f"Header: {header}")

        reader = csv.reader(f)
        for i, row in enumerate(reader):
            # prompt, contributor, comment = 3 columns
            if len(row) != 3:
                print(f"Row {i+2} has {len(row)} columns! Expected 3.")
                print(f"Content: {row}")

def main():
    validate_csv("chatgpt-text/prompts.csv")

if __name__ == "__main__":
    main()
