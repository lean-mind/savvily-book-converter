import re
from pdfminer.high_level import extract_text

full_text = extract_text("output/python_print.pdf")
raw_pdf = [line for line in full_text.splitlines() if line]


def get_page_numbers_of_headers_in_chapter(chapter_number: int) -> list:
    page_numbers_preceding_pages_with_headers: list = [
        raw_pdf[raw_pdf.index(line) - 1]
        for line in raw_pdf
        if line == get_heading_from_manuscript_for_chapter(chapter_number).upper()
    ]

    page_numbers_with_headers: list = [
        int(page_number) + 1
        for page_number in page_numbers_preceding_pages_with_headers
    ]

    return page_numbers_with_headers


def get_heading_from_manuscript_for_chapter(chapter_number: int) -> str:
    search_pattern = r"# (.*)\n"
    with open(f"sample-manuscript/0{chapter_number}_chapter.md", "r") as f:
        lines = f.readlines()
    for line in lines:
        if re.match(search_pattern, line):
            return re.match(search_pattern, line).group(1)
