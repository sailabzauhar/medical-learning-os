from pathlib import Path
import pdfplumber


PDF_PATH = "data/raw_pdf/Standard_Treatment_Guidelines_2013.pdf"
OUTPUT_DIR = Path("data/chapters")

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

CHAPTERS = [
    ("01_rational_use_of_medicines", 17, 26),
    ("02_common_conditions", 27, 62),
    ("03_emergency_conditions", 63, 95),
    ("04_cardiovascular_diseases", 96, 106),
    ("05_central_nervous_system_diseases", 107, 122),
    ("06_genitourinary_diseases", 123, 127),
    ("07_endocrine_diseases", 128, 140),
    ("08_gastrointestinal_diseases", 141, 153),
    ("09_infections", 154, 171),
    ("10_ent_diseases", 172, 184),
    ("11_eye_diseases", 185, 211),
    ("12_skin_diseases", 212, 236),
    ("13_obstetrics_and_gynecology", 237, 291),
    ("14_psychiatry_disorders", 292, 315),
    ("15_orthopedic_conditions", 316, 324),
    ("16_surgery", 325, 355),
    ("17_respiratory_diseases", 356, 372),
    ("18_pediatrics", 373, 423),
    ("19_dental_diseases", 424, 431),

]


def extract_chapter(pdf, start_page, end_page):
    text = []

    for page_no in range(start_page - 1, end_page):
        page_text = pdf.pages[page_no].extract_text()

        if page_text:
            text.append(page_text)

    return "\n\n".join(text)


with pdfplumber.open(PDF_PATH) as pdf:

    for chapter_name, start_page, end_page in CHAPTERS:

        print(f"Extracting {chapter_name}")

        chapter_text = extract_chapter(
            pdf,
            start_page,
            end_page
        )

        output_file = OUTPUT_DIR / f"{chapter_name}.txt"

        output_file.write_text(
            chapter_text,
            encoding="utf-8"
        )

print("All chapters extracted.")