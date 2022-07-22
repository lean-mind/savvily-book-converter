import re
import zipfile as epub_explorer


class EpubHelper:
    def __init__(self, ebook):
        self.ebook = ebook

    def get_chapter_lines_by_index(self, index: int) -> list:
        full_content = epub_explorer.ZipFile("output/ebook.epub").namelist()
        chapters_list: list = [
            ebook_item.replace("EPUB/", "")
            for ebook_item in full_content
            if (ebook_item.startswith("EPUB/text/ch"))
        ]
        chapter_one = self.ebook.get_item_with_href(chapters_list[index])
        chapter_one_text: str = chapter_one.get_content().decode()
        return chapter_one_text.splitlines()

    def get_h1_headings_from_first_chapter(self) -> list:
        h1_headings: str = "\n".join(
            line
            for line in self.get_chapter_lines_by_index(0)
            if (line.startswith("<h1"))
        )
        return h1_headings.split("\n")

    def get_value_from_manuscript_config_file(self, field_name: str) -> str:
        field_name_plus_separator: str = f"{field_name} = "
        field_value_group: str = "(.*)"
        search_pattern: str = f"{field_name_plus_separator}{field_value_group}"
        with open("sample-manuscript/resources/pub-data", "r") as f:
            lines = f.readlines()
        return self.find_pattern_in_list(search_pattern, lines)

    def find_pattern_in_list(self, pattern: str, lst: list) -> list:
        return [
            re.match(pattern, line).group(1)
            for line in lst
            if re.match(pattern, line)
        ]
