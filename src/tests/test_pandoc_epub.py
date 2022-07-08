import subprocess
from ebooklib import epub
import zipfile as epub_explorer
import pytest
import re

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
        config_title = get_value_from_manuscript_config_file("Title")
        assert metadata_title == config_title


@pytest.fixture
def get_h1_headings_from_first_chapter() -> list:
    h1_headings: str = "\n".join(
        line for line in get_chapter_lines_by_index(0) if (line.startswith("<h1"))
    )
    return h1_headings.split("\n")


def get_chapter_lines_by_index(index: int) -> list:
    full_content = epub_explorer.ZipFile("output/ebook.epub").namelist()
    chapters_list: list = [
        ebook_item.replace("EPUB/", "")
        for ebook_item in full_content
        if (ebook_item.startswith("EPUB/text/ch"))
    ]
    chapter_one = ebook.get_item_with_href(chapters_list[index])
    chapter_one_text: str = chapter_one.get_content().decode()
    return chapter_one_text.splitlines()


def get_value_from_manuscript_config_file(field_name: str) -> str:
    field_name_plus_separator: str = f"{field_name} = "
    field_value_group: str = "(.*)"
    search_pattern: str = f"{field_name_plus_separator}{field_value_group}"
    with open("sample-manuscript/resources/pub-data", "r") as f:
        lines = f.readlines()
    for line in lines:
        if re.match(search_pattern, line):
            return re.match(search_pattern, line).group(1)
