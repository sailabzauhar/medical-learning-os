import json
from pathlib import Path

from services.gemini_service import generate


# =========================
# CONFIG
# =========================

CHAPTER_FILE = Path(
    "data/chapters/17_respiratory_diseases.txt"
)

SUMMARY_PROMPT_FILE = Path(
    "prompts/summary_prompt.txt"
)

MCQ_PROMPT_FILE = Path(
    "prompts/mcq_prompt.txt"
)

OUTPUT_DIR = Path(
    "data/content"
)


# =========================
# LOAD CHAPTER
# =========================

print("Loading chapter...")

chapter_text = CHAPTER_FILE.read_text(
    encoding="utf-8"
)

chapter_title = (
    CHAPTER_FILE.stem
    .replace("_", " ")
    .title()
)


# =========================
# LOAD SUMMARY PROMPT
# =========================

summary_prompt = SUMMARY_PROMPT_FILE.read_text(
    encoding="utf-8"
)

summary_input = f"""
{summary_prompt}

CHAPTER TEXT

{chapter_text}
"""


# =========================
# GENERATE SUMMARY
# =========================

print("Generating summary...")

summary = generate(
    summary_input
)

print("Summary generated.")


# =========================
# LOAD MCQ PROMPT
# =========================

mcq_prompt = MCQ_PROMPT_FILE.read_text(
    encoding="utf-8"
)

mcq_input = f"""
{mcq_prompt}

CHAPTER TEXT

{chapter_text}
"""


# =========================
# GENERATE MCQS
# =========================

print("Generating MCQs...")

response = generate(
    mcq_input
)

response = response.strip()

response = response.replace(
    "```json",
    ""
)

response = response.replace(
    "```",
    ""
)

response = response.strip()

start = response.find("[")
end = response.rfind("]")

if start != -1 and end != -1:
    response = response[start:end + 1]


# =========================
# PARSE MCQ JSON
# =========================

try:

    mcqs = json.loads(response)

except Exception as e:

    error_file = OUTPUT_DIR / (
        CHAPTER_FILE.stem +
        "_mcq_error.txt"
    )

    error_file.write_text(
        response,
        encoding="utf-8"
    )

    raise Exception(
        f"MCQ JSON parsing failed. "
        f"Saved raw response to {error_file}"
    )


# =========================
# BUILD FINAL CHAPTER JSON
# =========================

chapter_data = {
    "chapter_title": chapter_title,
    "summary": {
        "content": summary
    },
    "mcq_count": len(mcqs),
    "mcqs": mcqs
}


# =========================
# SAVE OUTPUT
# =========================

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)

output_file = OUTPUT_DIR / (
    CHAPTER_FILE.stem + ".json"
)

with open(
    output_file,
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        chapter_data,
        f,
        indent=2,
        ensure_ascii=False
    )

print("\nSUCCESS")
print(f"Chapter: {chapter_title}")
print(f"MCQs: {len(mcqs)}")
print(f"Saved: {output_file}")