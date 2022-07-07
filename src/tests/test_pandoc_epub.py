import subprocess
from ebooklib import epub
import zipfile as epub_explorer


class EpubHelper:
    ebook: epub.EpubBook

    def __init__(self):
        subprocess.run(["./convert.sh", "-e"], check=True)
        self.ebook = epub.read_epub("output/ebook.epub")

    def chapters_href(self) -> list:
        full_content = epub_explorer.ZipFile("output/ebook.epub").namelist()
        return [
            ebook_item.replace("EPUB/", "")
            for ebook_item in full_content
            if (ebook_item.startswith("EPUB/text/ch"))
        ]

    def get_first_chapter(self):
        return self.ebook.get_item_with_href(self.chapters_href()[0])


class TestPandocEpubOutput:
    class TestHeadings:
        helper = EpubHelper()
        chapter_one = helper.get_first_chapter()
        chapter_one_text: str = chapter_one.get_content().decode()
        h1_headings: str = "\n".join(
            line for line in chapter_one_text.splitlines() if (line.startswith("<h1"))
        )

        def test_only_one_h1_header_in_first_chapter(self):
            number_of_h1_headings = self.h1_headings.split("\n")
            assert len(number_of_h1_headings) == 1

        def test_h1_header_works(self):
            expected_h1 = ">Est versat sed remorum ordine murice<"
            assert expected_h1 in self.h1_headings
