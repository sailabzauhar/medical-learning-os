from pathlib import Path
from services.gemini_service import generate


# ===== FILE PATHS =====

PROMPT_PATH = Path("prompts/summary_prompt.txt")

CHAPTER_PATH = Path(
    "data/chapters/17_respiratory_diseases.txt"
)

OUTPUT_PATH = Path(
    "data/content/17_respiratory_diseases_summary.md"
)


# ===== LOAD FILES =====

print("Loading prompt...")
summary_prompt = PROMPT_PATH.read_text(
    encoding="utf-8"
)

print("Loading chapter...")
chapter_text = CHAPTER_PATH.read_text(
    encoding="utf-8"
)


# ===== BUILD FINAL PROMPT =====

final_prompt = f"""
{summary_prompt}

=========================
CHAPTER TEXT
=========================

{chapter_text}
"""


# ===== GENERATE SUMMARY =====

print("Generating summary with Gemini...")

summary = generate(
    final_prompt
)


# ===== SAVE OUTPUT =====

OUTPUT_PATH.parent.mkdir(
    parents=True,
    exist_ok=True
)

OUTPUT_PATH.write_text(
    summary,
    encoding="utf-8"
)

print(
    f"Summary saved successfully -> {OUTPUT_PATH}"
)