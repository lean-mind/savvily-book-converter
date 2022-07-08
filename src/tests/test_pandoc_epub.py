import subprocess
from ebooklib import epub, ITEM_COVER
import pytest
import tests.epub_helper as helper

subprocess.run(["./convert.sh", "-e"], check=True)
ebook = epub.read_epub("output/ebook.epub")


@pytest.mark.usefixtures("get_h1_headings_from_first_chapter")
class TestHeadings:
    def test_only_one_h1_header_in_first_chapter(
        self, get_h1_headings_from_first_chapter
    ):
        number_of_h1_headings = len(get_h1_headings_from_first_chapter)
        assert number_of_h1_headings == 1

    def test_h1_header_content(self, get_h1_headings_from_first_chapter):
        expected_h1 = ">Est versat sed remorum ordine murice<"
        assert expected_h1 in get_h1_headings_from_first_chapter[0]


class TestMetadata:
    @pytest.mark.skip(reason="Currently reading from metadata.yml")
    def test_metadata_is_read_from_manuscript_config_file(self):
        metadata_title = ebook.get_metadata("DC", "title")[0][0]
        config_title = helper.get_value_from_manuscript_config_file("Title")
        assert metadata_title == config_title


class TestImages:
    cover_image_items = list(ebook.get_items_of_type(ITEM_COVER))

    def test_only_one_cover_image(self):
        assert len(self.cover_image_items) == 1

    def test_cover_image_is_rendered(self):
        expected_cover_image_filename = "book-cover-print.png"
        cover_image_name = self.cover_image_items[0].get_name()
        assert expected_cover_image_filename in cover_image_name


@pytest.fixture
def get_h1_headings_from_first_chapter() -> list:
    h1_headings: str = "\n".join(
        line
        for line in helper.get_chapter_lines_by_index(0)
        if (line.startswith("<h1"))
    )
    return h1_headings.split("\n")
