from pdfminer.high_level import extract_text


class TestPandocPdfOutput:
    raw_text = extract_text(
        "output/codigo_sostenible_savvily/codigo_sostenible_savvily.pdf"
    )
    text_without_empty_lines = [line for line in raw_text.splitlines() if line]

    def test_total_page_number(self):
        last_line = self.text_without_empty_lines[-1]
        expected_number_of_pages = 19
        number_of_closing_blank_pages = 3
        assert (
            int(last_line) + number_of_closing_blank_pages == expected_number_of_pages
        )

    def test_code_block_lang_capitalized(self):
        code_block_tags = [
            tag for tag in self.text_without_empty_lines if tag.lower() == "java"
        ]
        lower_cased_tags = [
            lower for lower in code_block_tags if not lower[0].isupper()
        ]
        assert len(lower_cased_tags) == 0
