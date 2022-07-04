import src.manuscriptFormatter as formatter
import src.tests.expected_output_md as expected


class TestFormatter:
    def test_new_ebook_format(self):
        assert (
            formatter.get_formatted_md_for_epub_as_stream("sample-manuscript")
            .read()
            .decode()
            == expected.epub_format
        )

    def test_new_pdf_print_format(self):
        assert (
            formatter.get_formatted_manuscript_stream_for_print_pdf("sample-manuscript")
            .read()
            .decode()
            == expected.pdf_print
        )

    def test_new_pdf_screen_format(self):
        assert (
            formatter.get_formatted_manuscript_stream_for_screen_pdf(
                "sample-manuscript"
            )
            .read()
            .decode()
            == expected.pdf_screen
        )
