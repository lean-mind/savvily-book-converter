import os
import re


class ManuscriptReader:
    def __init__(self, path: str):
        self.path = path

    def read(self) -> str:
        manuscript_files = self.get_sorted_chapters()
        chapters = []
        for file in manuscript_files:
            with open(f"{self.path}/{file}", "r") as f:
                chapters.append(self._list_to_string(f.readlines()))
        book_as_string = self._list_to_string(chapters)
        return book_as_string

    def read_chapters(self, chapters: list) -> str:
        read_chapters = []
        for file in chapters:
            with open(f"{self.path}/{file}", "r") as f:
                read_chapters.append(self._list_to_string(f.readlines()))
        chapters_as_string = self._list_to_string(read_chapters)
        return chapters_as_string

    def get_sorted_chapters(self) -> list:
        dir_list = os.listdir(self.path)
        return sorted(
            [file for file in dir_list if re.match(r"\d\d_.*\.md|\d\d_.*\.txt", file)]
        )

    def _list_to_string(self, string_list: list) -> str:
        return "".join(string_list)
