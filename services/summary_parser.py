import re


def extract_subtopics(summary_text):

    pattern = r"(?=^## )"

    sections = re.split(
        pattern,
        summary_text,
        flags=re.MULTILINE
    )

    subtopics = []

    for section in sections:

        section = section.strip()

        if not section.startswith("## "):
            continue

        lines = section.split("\n")

        title = lines[0].replace(
            "## ",
            ""
        ).strip()

        content = "\n".join(
            lines[1:]
        ).strip()

        subtopics.append({
            "title": title,
            "content": content
        })

    return subtopics