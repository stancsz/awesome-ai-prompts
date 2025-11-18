# Awesome AI Prompts

This repository collects high-quality, tested prompts for popular generative AI services. Each subfolder focuses on a specific provider so entries stay organized and easy to browse.

## Structure

- `midjourney/` - Prompts tailored for Midjourney image generation.
- `google-nano-banana/` - A folder for Google Nano Banana experiments.
- `stable-diffusion/` - Collections for Stable Diffusion workflows and checkpoints.
- `chatgpt/text/` - Text-based ChatGPT prompts covering conversations, coding assistance, and reasoning tasks.
- `chatgpt/image/` - Image-focused prompts for ChatGPT Vision or DALL-E-style generation.
- `gemini/text/` - Text-first prompts tailored to Gemini's instruction and planning abilities.
- `gemini/image/` - Multimodal prompts for Gemini's vision and text-to-image experiments.
- `dalle/` - DALL-E prompt ideas and formatting notes.
- `claude/` - Behavior, tone, and safety prompts for Claude models.
- `agentic-coding/` - Agentic workflows where models plan, execute, and refine coding tasks.

Contributions welcome via pull requests; please name files clearly and include source/context for each prompt.

## Contributing

Contributions should be submitted as UTF-8 encoded CSV files to the appropriate provider directory (for example `chatgpt/text/`, `gemini/image/`, etc.). Each CSV must have the exact header (first line):

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
"Summarize the following article:\n[article text]",@alice,"summarization"

Workflow:
1. Create or update a CSV file in the appropriate provider directory following the rules above.
2. Open a pull request that explains the prompt’s purpose, model tested against, and any results you observed.
3. Use descriptive filenames and organize prompts by intent or category where helpful.
4. Reviewers may reformat or reject submissions that do not follow the CSV rules.

This format ensures consistent, machine-readable contributions and makes it easy to curate and import prompts programmatically.
