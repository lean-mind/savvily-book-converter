from ebooklib import epub
import zipfile as epub_explorer

epub_path = '../output/ebook.epub'
book = epub.read_epub(epub_path)


def chapters_href() -> list:
    full_content = epub_explorer.ZipFile(epub_path).namelist()
    return [ebook_item.replace('EPUB/', '')
            for ebook_item in full_content
            if (ebook_item.startswith('EPUB/text/ch'))]


class TestPandocEpubOutput:

    class TestHeadings:
        first_chapter_href: str = chapters_href()[0]
        chapter_one = book.get_item_with_href(first_chapter_href)
        chapter_one_text: str = chapter_one.get_content().decode()
        h1_headings: str = '\n'.join(line for line in chapter_one_text.splitlines() if (line.startswith('<h1')))

        def test_only_one_h1_header_in_first_chapter(self):
            number_of_h1_headings = self.h1_headings.split('\n')
            assert len(number_of_h1_headings) == 1

        def test_h1_header_works(self):
            expected_h1 = '>Est versat sed remorum ordine murice<'
            assert expected_h1 in self.h1_headings
