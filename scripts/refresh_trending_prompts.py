import csv
import io
import os
from datetime import datetime
from pathlib import Path
from typing import List, Tuple

from dotenv import load_dotenv
from openai import OpenAI
from perplexity import Perplexity

BASE_DIR = Path(__file__).resolve().parent.parent
CSV_HEADER = ["prompt", "contributor", "comment"]
README_PATH = BASE_DIR / "README.md"
TRENDING_HEADING = "## Trending Prompts Today"
STRUCTURE_HEADING = "## Structure"
DEFAULT_CONTRIBUTOR = "@trend-bot"


def load_clients() -> Tuple[Perplexity, OpenAI]:
    load_dotenv(BASE_DIR / ".env")
    perplexity_key = os.getenv("PERPLEXITY_API_KEY")
    openai_key = os.getenv("OPENAI_API_KEY")
    missing = [name for name, value in (("PERPLEXITY_API_KEY", perplexity_key), ("OPENAI_API_KEY", openai_key)) if not value]
    if missing:
        raise RuntimeError(f"Missing required environment variables: {', '.join(missing)}")

    perplexity_client = Perplexity(api_key=perplexity_key)
    openai_client = OpenAI(api_key=openai_key)
    return perplexity_client, openai_client


def discover_prompt_dirs(base: Path) -> List[Path]:
    csv_paths = sorted(base.glob("**/prompts.csv"))
    dirs = []
    for d in sorted({p.parent for p in csv_paths}):
        # Exclude any prompts.csv located under the scripts/ folder to avoid
        # treating scripts as prompt providers.
        if "scripts" in d.parts:
            continue
        dirs.append(d)
    return dirs


def ensure_csv(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists() or path.stat().st_size == 0:
        with path.open("w", encoding="utf-8", newline="") as fh:
            csv.writer(fh).writerow(CSV_HEADER)


def read_existing_prompts(path: Path) -> set:
    prompts = set()
    if not path.exists():
        return prompts
    with path.open(encoding="utf-8", newline="") as fh:
        reader = csv.reader(fh)
        next(reader, None)
        for row in reader:
            if not row:
                continue
            prompts.add(row[0].strip())
    return prompts


def summarize_perplexity(perplexity_client: Perplexity, query: str) -> str:
    search = perplexity_client.search.create(
        query=query,
        max_results=8,
        max_tokens_per_page=1024
    )
    lines = []
    results = getattr(search, "results", []) or []
    for idx, result in enumerate(results, start=1):
        title = getattr(result, "title", f"Result {idx}")
        url = getattr(result, "url", "")
        snippet = getattr(result, "snippet", "")
        lines.append(f"Result {idx}: {title}")
        if url:
            lines.append(f"URL: {url}")
        if snippet:
            lines.append(snippet)
        lines.append("")
    return "\n".join(lines).strip()


def synthesize_prompts(openai_client: OpenAI, folder_label: str, context: str) -> List[dict]:
    prompt_text = f"""You are asked to produce the top 10 trending prompts for {folder_label}. Use the Perplexity search context below. Output exactly 10 CSV rows with the header prompt,contributor,comment. The contributor field should default to {DEFAULT_CONTRIBUTOR} if no human handle is evident. Comments should briefly describe why the prompt is trending or note a source when relevant. Do not include any extra explanation outside the CSV data itself.

Perplexity context:
{context}
"""

    response = openai_client.responses.create(
        model="gpt-5-mini",
        input=[{"role": "user", "content": prompt_text}],
        text={"format": {"type": "text"}, "verbosity": "medium"},
        reasoning={"effort": "medium", "summary": "auto"},
        tools=[],
        store=True,
        include=["reasoning.encrypted_content", "web_search_call.action.sources"]
    )

    output_text = getattr(response, "output_text", "") or ""
    if not output_text:
        output_chunks = []
        for chunk_group in response.output or []:
            for chunk in getattr(chunk_group, "content", []):
                if getattr(chunk, "type", None) == "output_text":
                    output_chunks.append(getattr(chunk, "text", ""))
        output_text = "".join(output_chunks).strip()

    if not output_text:
        raise RuntimeError(f"No text output from OpenAI for {folder_label}")

    header_idx = output_text.lower().find(",".join(CSV_HEADER))
    csv_text = output_text[header_idx:] if header_idx != -1 else output_text
    reader = csv.reader(io.StringIO(csv_text))
    rows = [row for row in reader if row]
    if rows and rows[0][0].lower() == "prompt":
        rows = rows[1:]

    processed = []
    for row in rows[:10]:
        padded = (row + [""] * len(CSV_HEADER))[: len(CSV_HEADER)]
        prompt_value = padded[0].strip()
        if not prompt_value:
            continue
        processed.append(
            {
                "prompt": prompt_value,
                "contributor": padded[1].strip() or DEFAULT_CONTRIBUTOR,
                "comment": padded[2].strip(),
            }
        )
    return processed


def append_new_prompts(csv_path: Path, entries: List[dict], existing: set) -> List[dict]:
    new_rows = []
    if not entries:
        return new_rows
    ensure_csv(csv_path)
    with csv_path.open("a", encoding="utf-8", newline="") as fh:
        writer = csv.writer(fh)
        for entry in entries:
            if entry["prompt"] in existing:
                continue
            writer.writerow([entry["prompt"], entry["contributor"], entry["comment"]])
            existing.add(entry["prompt"])
            new_rows.append(entry)
    return new_rows


def build_readme_section(trending_data: List[Tuple[str, List[dict]]]) -> str:
    lines = [TRENDING_HEADING, "", f"Last refreshed: {datetime.utcnow():%Y-%m-%d %H:%M UTC}", ""]
    if not trending_data:
        lines.append("Run `python scripts/refresh_trending_prompts.py` to populate this section.")
        return "\n".join(lines).rstrip() + "\n"

    for label, entries in trending_data:
        lines.append(f"### {label}")
        lines.append("")
        if not entries:
            lines.append("No new trending prompts could be generated for this category.")
        else:
            for idx, entry in enumerate(entries, start=1):
                comment = f" - {entry['comment']}" if entry["comment"] else ""
                lines.append(
                    f"{idx}. {entry['prompt']} ({entry['contributor']}){comment}"
                )
        lines.append("")
    lines.append("To regenerate the list above, rerun `python scripts/refresh_trending_prompts.py` after ensuring the required API keys are available in `.env`.")
    return "\n".join(lines).rstrip() + "\n"


def update_readme(trending_section: str) -> None:
    if not README_PATH.exists():
        raise FileNotFoundError("README.md not found in repository root.")

    content = README_PATH.read_text(encoding="utf-8")
    start = content.find(TRENDING_HEADING)
    if start == -1:
        raise RuntimeError(f"{TRENDING_HEADING} not found in README.md")

    end = content.find(STRUCTURE_HEADING, start)
    if end == -1:
        raise RuntimeError(f"{STRUCTURE_HEADING} not found; cannot replace trending section.")

    new_content = content[:start] + trending_section + "\n" + content[end:]
    README_PATH.write_text(new_content, encoding="utf-8")


def main() -> None:
    perplexity_client, openai_client = load_clients()
    prompt_dirs = discover_prompt_dirs(BASE_DIR)
    if not prompt_dirs:
        print("No prompt directories found.")
        return

    trending_info = []
    for directory in prompt_dirs:
        folder_label = str(directory.relative_to(BASE_DIR)).replace("\\", "/")
        print(f"Gathering trends for {folder_label}...")
        csv_path = directory / "prompts.csv"
        ensure_csv(csv_path)
        existing = read_existing_prompts(csv_path)

        query = f"top 10 trending ai prompts for today for {folder_label}"
        context = summarize_perplexity(perplexity_client, query)
        prompts = synthesize_prompts(openai_client, folder_label, context)
        appended = append_new_prompts(csv_path, prompts, existing)

        if appended:
            print(f"  Appended {len(appended)} new prompts to {csv_path}")
        else:
            print(f"  No new prompts to append to {csv_path}")

        trending_info.append((folder_label, prompts))

    section = build_readme_section(trending_info)
    update_readme(section)
    print("Updated README.trending section.")


if __name__ == "__main__":
    main()
