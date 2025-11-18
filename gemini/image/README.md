# gemini/image

Vision and text-to-image prompts for Gemini's multimodal models.

Contributions to this directory should be submitted as UTF-8 encoded CSV files with the exact header (first line):

prompt,contributor,comment

Rules:
- Header order must be exactly: prompt,contributor,comment
- Each CSV row is a single prompt entry.
- Fields that contain commas, double quotes, or newlines must be wrapped in double quotes.
- Escape double quotes by doubling them (e.g., "He said ""hello""").
- Use a short contributor handle (e.g., @alice) or `@curated` for curated entries in the contributor field.
- Keep comment as a short tag or note (optional).
- Preserve newlines inside quoted fields for multiline prompts.

Example row:
"Create a photorealistic scene of a mountain lake at golden hour, with mist rising and kayakers in the distance.",@alice,"photorealism"

Follow the top-level repository CONTRIBUTING guidelines when opening pull requests. Reviewers may reformat or reject submissions that do not follow the CSV rules.
