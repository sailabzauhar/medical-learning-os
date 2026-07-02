import json
from pathlib import Path


CHAPTER_TITLE = "Respiratory Diseases"

SUMMARY_PATH = Path(
    "data/content/17_respiratory_diseases_summary.md"
)

MCQ_PATH = Path(
    "data/content/17_respiratory_diseases_mcqs.json"
)

OUTPUT_PATH = Path(
    "data/content/17_respiratory_diseases.json"
)


print("Loading summary...")

summary = SUMMARY_PATH.read_text(
    encoding="utf-8"
)

print("Loading MCQs...")

with open(
    MCQ_PATH,
    "r",
    encoding="utf-8"
) as f:

    mcqs = json.load(f)


chapter_data = {
    "chapter_title": CHAPTER_TITLE,
    "summary": {
        "content": summary
    },
    "mcqs": mcqs
}


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
        chapter_data,
        f,
        indent=2,
        ensure_ascii=False
    )

print(
    f"Saved -> {OUTPUT_PATH}"
)