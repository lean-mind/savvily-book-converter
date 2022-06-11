from pdfminer.high_level import extract_text


class Test_pandoc_pdf_output:

    def test_total_page_number(self):
        raw_text = extract_text('../output/codigo_sostenible_savvily/codigo_sostenible_savvily.pdf')
        text_without_empty_lines = [line
                                    for line in raw_text.splitlines()
                                    if line]
        last_line = text_without_empty_lines[-1]

        expected_number_of_pages = 19
        number_of_closing_blank_pages = 3
        assert int(last_line) + number_of_closing_blank_pages == expected_number_of_pages
