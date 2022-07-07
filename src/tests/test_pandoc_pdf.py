import subprocess
from pdfminer.high_level import extract_text
from pdfminer.utils import AnyIO


class TestPandocPdfOutput:
    raw_pdf: AnyIO
    subprocess.run(["./convert.sh", "-p"], check=True)
    full_text = extract_text("output/python_print.pdf")
    raw_pdf = [line for line in full_text.splitlines() if line]

    def test_total_page_number(self):
        last_line = self.raw_pdf[-1]
        expected_number_of_pages = 19
        number_of_closing_blank_pages = 3
        assert (
            int(last_line) + number_of_closing_blank_pages == expected_number_of_pages
        )

    def test_code_block_lang_capitalized(self):
        code_block_tags = [tag for tag in self.raw_pdf if tag.lower() == "java"]
        lower_cased_tags = [
            lower for lower in code_block_tags if not lower[0].isupper()
        ]
        assert len(lower_cased_tags) == 0
