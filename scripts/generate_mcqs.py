import json
from pathlib import Path

from services.gemini_service import generate


PROMPT_PATH = Path("prompts/mcq_prompt.txt")

CHAPTER_PATH = Path(
    "data/chapters/17_respiratory_diseases.txt"
)

OUTPUT_PATH = Path(
    "data/content/17_respiratory_diseases_mcqs.json"
)


print("Loading MCQ prompt...")
mcq_prompt = PROMPT_PATH.read_text(
    encoding="utf-8"
)

print("Loading chapter...")
chapter_text = CHAPTER_PATH.read_text(
    encoding="utf-8"
)

final_prompt = f"""
{mcq_prompt}

CHAPTER TEXT

{chapter_text}
"""

print("Generating MCQs...")

response = generate(
    final_prompt
)
response = response.replace("```json", "")
response = response.replace("```", "")
response = response.strip()

try:

    mcqs = json.loads(response)

except Exception as e:

    print("JSON parsing failed")

    Path(
        "data/content/mcq_error_output.txt"
    ).write_text(
        response,
        encoding="utf-8"
    )

    raise e


OUTPUT_PATH.parent.mkdir(
    parents=True,
    exist_ok=True
)

with open(
    OUTPUT_PATH,
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        mcqs,
        f,
        indent=2,
        ensure_ascii=False
    )

print(
    f"Saved -> {OUTPUT_PATH}"
)

print(
    f"MCQs generated: {len(mcqs)}"
)