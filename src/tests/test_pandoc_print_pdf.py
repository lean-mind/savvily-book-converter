import pytest
from pdfminer.high_level import extract_text
from tests.PdfHelper import PdfHelper

full_text = extract_text("output/python_print.pdf")
raw_pdf: list = [line for line in full_text.splitlines() if line]
helper = PdfHelper(raw_pdf)


class TestPrintOutput:
    def test_total_page_number(self):
        expected_number_of_pages: int = 19
        last_line: str = raw_pdf[-1]
        number_of_closing_blank_pages: int = 3
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

    def test_chapter_name_in_headers_of_odd_numbered_pages(self):
        for page_number in helper.get_page_numbers_of_headers_in_chapter(1):
            assert page_number % 2 != 0

    def test_all_links_are_footnotes(self):
        links_in_pdf = helper.get_links_from_pdf()

        links_as_footnotes = [link for link in links_in_pdf if link[0].isdigit()]

        assert links_as_footnotes == links_in_pdf

    @pytest.mark.skip(reason="Currently broken, links in the same line are swallowed")
    def test_all_links_are_rendered_as_footnotes(self):
        links_ch1 = helper.get_links_from_manuscript_for_chapter(1)
        links_ch2 = helper.get_links_from_manuscript_for_chapter(2)
        all_links_in_manuscript = links_ch1 + links_ch2

        links_in_pdf = helper.get_links_from_pdf()

        assert len(all_links_in_manuscript) == len(links_in_pdf)
