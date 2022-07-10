import re


class PdfHelper:
    def __init__(self, raw_pdf):
        self.raw_pdf = raw_pdf

    def get_links_from_pdf(self) -> list:
        link_pattern = r"(.*http://.*)"
        links = [
            re.match(link_pattern, line).group(1)
            for line in self.raw_pdf
            if re.match(link_pattern, line)
        ]
        return links

    def get_page_numbers_of_headers_in_chapter(self, chapter_number: int) -> list:
        page_numbers_preceding_pages_with_headers: list = [
            self.raw_pdf[index - 1]
            for index, line in enumerate(self.raw_pdf)
            if line == self.get_heading_from_manuscript_for_chapter(1).upper()
        ]
        page_numbers_with_headers: list = [
            int(page_number) + 1
            for page_number in page_numbers_preceding_pages_with_headers
        ]
        return page_numbers_with_headers

    def get_heading_from_manuscript_for_chapter(self, chapter_number: int) -> str:
        heading_pattern = r"# (.*)\n"
        with open(f"sample-manuscript/0{chapter_number}_chapter.md", "r") as f:
            lines = f.readlines()
        for line in lines:
            if re.match(heading_pattern, line):
                return re.match(heading_pattern, line).group(1)

    def get_links_from_manuscript_for_chapter(self, chapter_number: int) -> list:
        link_pattern = r".*(http://.*)\)"
        with open(f"sample-manuscript/0{chapter_number}_chapter.md", "r") as f:
            lines = f.readlines()
        links = [
            re.match(link_pattern, line).group(1)
            for line in lines
            if re.match(link_pattern, line)
        ]
        return links
