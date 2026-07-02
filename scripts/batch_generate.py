import json
import time
from pathlib import Path

from services.gemini_service import generate


# =========================
# CONFIG
# =========================

CHAPTER_DIR = Path("data/chapters")

OUTPUT_DIR = Path("data/content")

SUMMARY_PROMPT_FILE = Path(
    "prompts/summary_prompt.txt"
)

MCQ_PROMPT_FILE = Path(
    "prompts/mcq_prompt.txt"
)

LOG_FILE = Path(
    "logs/batch_generation.log"
)

MAX_RETRIES = 2

SLEEP_BETWEEN_CHAPTERS = 2


# =========================
# SETUP
# =========================

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)

LOG_FILE.parent.mkdir(
    parents=True,
    exist_ok=True
)

summary_prompt = SUMMARY_PROMPT_FILE.read_text(
    encoding="utf-8"
)

mcq_prompt = MCQ_PROMPT_FILE.read_text(
    encoding="utf-8"
)


# =========================
# LOGGER
# =========================

def log(message):

    print(message)

    with open(
        LOG_FILE,
        "a",
        encoding="utf-8"
    ) as f:

        f.write(message + "\n")


# =========================
# JSON CLEANER
# =========================

def clean_json_response(response):

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

    return response


# =========================
# JSON REPAIR
# =========================

def repair_json(bad_json):

    repair_prompt = f"""
You are a JSON repair tool.

The following text was intended to be a JSON array.

Repair it.

Rules:

1. Return ONLY valid JSON.
2. Do not add explanations.
3. Do not add markdown.
4. Do not remove MCQs.
5. Preserve all content.
6. Fix commas, quotes, brackets, escape characters,
   control characters, and formatting errors.

BAD JSON:

{bad_json}
"""

    repaired = generate(
        repair_prompt
    )

    repaired = clean_json_response(
        repaired
    )

    return json.loads(
        repaired
    )


# =========================
# PARSE MCQ JSON
# =========================

def parse_mcqs(response, chapter_file):

    response = clean_json_response(
        response
    )

    try:

        return json.loads(
            response
        )

    except Exception as e:

        log(
            f"JSON PARSE FAILED -> {chapter_file.name}"
        )

        raw_error_file = (
            OUTPUT_DIR /
            f"{chapter_file.stem}_RAW_JSON_ERROR.txt"
        )

        raw_error_file.write_text(
            response,
            encoding="utf-8"
        )

        log(
            "Attempting JSON repair..."
        )

        try:

            repaired_mcqs = repair_json(
                response
            )

            log(
                "JSON repair successful."
            )

            return repaired_mcqs

        except Exception as repair_error:

            raise Exception(
                f"JSON repair failed: {repair_error}"
            )


# =========================
# PROCESS CHAPTER
# =========================

def process_chapter(chapter_file):

    chapter_text = chapter_file.read_text(
        encoding="utf-8"
    )

    chapter_title = (
        chapter_file.stem
        .replace("_", " ")
        .title()
    )

    log(
        f"\nProcessing: {chapter_title}"
    )

    # =====================
    # SUMMARY
    # =====================

    summary_input = f"""
{summary_prompt}

CHAPTER TEXT

{chapter_text}
"""

    summary = generate(
        summary_input
    )

    # =====================
    # MCQ
    # =====================

    mcq_input = f"""
{mcq_prompt}

CHAPTER TEXT

{chapter_text}
"""

    response = generate(
        mcq_input
    )

    mcqs = parse_mcqs(
        response,
        chapter_file
    )

    # =====================
    # BUILD JSON
    # =====================

    chapter_json = {
        "chapter_title": chapter_title,
        "summary_word_count": len(
            summary.split()
        ),
        "mcq_count": len(
            mcqs
        ),
        "summary": {
            "content": summary
        },
        "mcqs": mcqs
    }

    output_file = (
        OUTPUT_DIR /
        f"{chapter_file.stem}.json"
    )

    with open(
        output_file,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            chapter_json,
            f,
            indent=2,
            ensure_ascii=False
        )

    # =====================
    # REMOVE OLD FAILED FILE
    # =====================

    failed_file = (
        OUTPUT_DIR /
        f"{chapter_file.stem}_FAILED.txt"
    )

    if failed_file.exists():

        try:

            failed_file.unlink()

            log(
                f"REMOVED -> {failed_file.name}"
            )

        except Exception as e:

            log(
                f"WARNING -> Could not remove "
                f"{failed_file.name}: {e}"
            )

    log(
        f"SUCCESS -> {output_file}"
    )


# =========================
# FIND PENDING CHAPTERS
# =========================

pending_chapters = []

for chapter_file in sorted(
    CHAPTER_DIR.glob("*.txt")
):

    output_file = (
        OUTPUT_DIR /
        f"{chapter_file.stem}.json"
    )

    if output_file.exists():

        log(
            f"SKIP -> {chapter_file.name}"
        )

        continue

    pending_chapters.append(
        chapter_file
    )

log(
    f"\nPending Chapters: {len(pending_chapters)}"
)


# =========================
# MAIN LOOP
# =========================

success = 0
failed = 0

for chapter_file in pending_chapters:

    retries = MAX_RETRIES

    while retries >= 0:

        try:

            process_chapter(
                chapter_file
            )

            success += 1

            break

        except Exception as e:

            error_text = str(e)

            log(
                f"ERROR -> {chapter_file.name}"
            )

            log(
                error_text
            )

            if (
                "RESOURCE_EXHAUSTED" in error_text
                or
                "monthly spending cap" in error_text
            ):

                log(
                    "\nSTOPPED: GEMINI SPENDING CAP EXCEEDED"
                )

                raise SystemExit()

            retries -= 1

            if retries < 0:

                failed += 1

                error_file = (
                    OUTPUT_DIR /
                    f"{chapter_file.stem}_FAILED.txt"
                )

                error_file.write_text(
                    error_text,
                    encoding="utf-8"
                )

                log(
                    f"FAILED -> {chapter_file.name}"
                )

            else:

                log(
                    f"Retrying... Remaining retries: {retries}"
                )

                time.sleep(5)

    time.sleep(
        SLEEP_BETWEEN_CHAPTERS
    )


# =========================
# FINAL SUMMARY
# =========================

log("\n====================")
log(f"SUCCESS : {success}")
log(f"FAILED  : {failed}")
log("====================")