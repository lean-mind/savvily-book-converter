import formatter.EpubFormatter as epubFormatter
import formatter.ScreenPDFFormatter as screenPdfFormatter
import formatter.PrintPDFFormatter as printPdfFormatter
import tests.expected_output_md as expected


class TestFormatter:
    def test_new_ebook_format(self):
        assert (
            epubFormatter.run("sample-manuscript").read().decode()
            == expected.epub_format
        )

    def test_new_pdf_print_format(self):
        assert (
            printPdfFormatter.run("sample-manuscript").read().decode()
            == expected.pdf_print
        )

    def test_new_pdf_screen_format(self):
        assert (
            screenPdfFormatter.run("sample-manuscript").read().decode()
            == expected.pdf_screen
        )
