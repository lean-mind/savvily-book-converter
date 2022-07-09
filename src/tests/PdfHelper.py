import re


class PdfHelper:
    def __init__(self, raw_pdf):
        self.raw_pdf = raw_pdf

    def get_links_from_pdf(self) -> list:
        search_pattern = r"(.*http://.*)"
        links = []
        for line in self.raw_pdf:
            if re.match(search_pattern, line):
                links.append(re.match(search_pattern, line).group(1))
        return links

    def get_page_numbers_of_headers_in_chapter(self, chapter_number: int) -> list:
        page_numbers_preceding_pages_with_headers: list = [
            self.raw_pdf[self.raw_pdf.index(line) - 1]
            for line in self.raw_pdf
            if line
            == self.get_heading_from_manuscript_for_chapter(chapter_number).upper()
        ]

        page_numbers_with_headers: list = [
            int(page_number) + 1
            for page_number in page_numbers_preceding_pages_with_headers
        ]

        return page_numbers_with_headers

    def get_heading_from_manuscript_for_chapter(self, chapter_number: int) -> str:
        search_pattern = r"# (.*)\n"
        with open(f"sample-manuscript/0{chapter_number}_chapter.md", "r") as f:
            lines = f.readlines()
        for line in lines:
            if re.match(search_pattern, line):
                return re.match(search_pattern, line).group(1)

    def get_links_from_manuscript_for_chapter(self, chapter_number: int) -> list:
        search_pattern = r".*(http://.*)\)"
        links = []
        with open(f"sample-manuscript/0{chapter_number}_chapter.md", "r") as f:
            lines = f.readlines()
        for line in lines:
            if re.match(search_pattern, line):
                links.append(re.match(search_pattern, line).group(1))
        return links
