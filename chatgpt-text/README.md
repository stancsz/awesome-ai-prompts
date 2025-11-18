# chatgpt-text

Text-focused ChatGPT prompts live here; keep each prompt file in the canonical CSV format listed below.

All prompt files in this directory must be UTF-8 encoded CSV files with the exact header (first line):

prompt,contributor,comment

Rules:
- Header order must be exactly: prompt,contributor,comment
- Each row represents a single prompt.
- Fields that contain commas, double quotes, or newlines must be wrapped in double quotes.
- Escape double quotes by doubling them (e.g., "He said ""hello""").
- Use a short contributor handle (e.g., @alice or an email) or use @curated for curated entries.
- Keep comment as a short tag or note (optional).
- Use UTF-8 encoding; preserve newlines inside quoted fields for multiline prompts.

Example row:
"Summarize the following article:\n[article text]",@alice,"summarization"

Please only add files that follow these rules so this directory remains easy to validate and consume programmatically.
