import subprocess
from pdfminer.high_level import extract_text
import tests.pdf_helper as helper


# TODO.Links to footnotes
class TestPrintOutput:
    subprocess.run(["./convert.sh", "-p"], check=True)
    full_text = extract_text("output/python_print.pdf")
    raw_pdf = [line for line in full_text.splitlines() if line]

    def test_total_page_number(self):
        expected_number_of_pages: int = 19
        last_line: str = self.raw_pdf[-1]
        number_of_closing_blank_pages: int = 3
        actual_number_of_pages: int = int(last_line) + number_of_closing_blank_pages
        assert actual_number_of_pages == expected_number_of_pages

    def test_code_block_lang_tag_capitalized(self):
        all_code_block_lang_tags: list = [
            tag for tag in self.raw_pdf if tag.lower() in ["java", "python"]
        ]
        capitalized_lang_tags: list = [
            capitalized_tag
            for capitalized_tag in all_code_block_lang_tags
            if capitalized_tag[0].isupper()
        ]
        assert len(capitalized_lang_tags) == len(all_code_block_lang_tags)

    def test_code_block_lang_tag_position(self):
        known_code_block_beginning: str = "if (61) {"
        code_block_position: int = self.raw_pdf.index(known_code_block_beginning)
        expected_code_block_lang_tag: str = "Java"
        actual_code_block_lang_tag: str = self.raw_pdf[code_block_position - 1]
        assert actual_code_block_lang_tag == expected_code_block_lang_tag

    def test_chapter_name_in_headers_of_odd_numbered_pages(self):
        for page_number in helper.get_page_numbers_of_headers_in_chapter(1):
            assert page_number % 2 != 0


# TODO.Links NOT in footnotes
# class TestScreenOutput:
