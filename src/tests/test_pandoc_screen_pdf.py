from pdfminer.high_level import extract_text
from tests.PdfHelper import PdfHelper

full_text = extract_text("output/python_screen.pdf")
raw_pdf: list = [line for line in full_text.splitlines() if line]
helper = PdfHelper(raw_pdf)


class TestPrintOutput:
    def test_total_page_number(self):
        expected_number_of_pages: int = 18
        number_of_watermark_fields: int = 3
        last_line: str = raw_pdf[-(1 + number_of_watermark_fields)]
        number_of_closing_blank_pages: int = 1
        actual_number_of_pages: int = int(last_line) + number_of_closing_blank_pages
        assert actual_number_of_pages == expected_number_of_pages

    def test_code_block_lang_tag_capitalized(self):
        all_code_block_lang_tags: list = [
            tag for tag in raw_pdf if tag.lower() in ["java", "python"]
        ]
        capitalized_lang_tags: list = [
            capitalized_tag
            for capitalized_tag in all_code_block_lang_tags
            if capitalized_tag[0].isupper()
        ]
        assert len(capitalized_lang_tags) == len(all_code_block_lang_tags)

    def test_lang_tag_precede_code_block(self):
        known_code_block_start: str = "if (61) {"
        code_block_position: int = raw_pdf.index(known_code_block_start)
        expected_code_block_lang_tag: str = "Java"
        actual_code_block_lang_tag: str = raw_pdf[code_block_position - 1]
        assert actual_code_block_lang_tag == expected_code_block_lang_tag

    def test_no_links_are_outside_references(self):
        links_in_pdf = helper.get_links_from_pdf()

        assert len(links_in_pdf) == 0
