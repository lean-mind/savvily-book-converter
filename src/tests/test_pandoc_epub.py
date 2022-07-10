from ebooklib import epub, ITEM_COVER
import pytest
from tests.EpubHelper import EpubHelper

ebook = epub.read_epub("output/ebook.epub")
helper = EpubHelper(ebook)


class TestHeadings:
    first_chapter_h1_headings: list = helper.get_h1_headings_from_first_chapter()

    def test_only_one_h1_header_in_first_chapter(self):
        number_of_h1_headings: int = len(self.first_chapter_h1_headings)
        assert number_of_h1_headings == 1

    def test_h1_header_content(self):
        expected_h1: str = ">Est versat sed remorum ordine murice<"
        assert expected_h1 in self.first_chapter_h1_headings[0]


class TestMetadata:
    @pytest.mark.skip(reason="Currently reading from metadata.yml")
    def test_metadata_is_read_from_manuscript_config_file(self):
        metadata_title = ebook.get_metadata("DC", "title")[0][0]
        config_title: str = helper.get_value_from_manuscript_config_file("Title")
        assert metadata_title == config_title


class TestImages:
    cover_image_items: list = list(ebook.get_items_of_type(ITEM_COVER))

    def test_only_one_cover_image(self):
        assert len(self.cover_image_items) == 1

    def test_cover_image_is_rendered(self):
        expected_cover_image_filename: str = "book-cover-print.png"
        cover_image_name: str = self.cover_image_items[0].get_name()
        assert expected_cover_image_filename in cover_image_name
