import os
import re


class ManuscriptReader:
    def __init__(self, path: str):
        self.path = path

    def read(self) -> str:
        chapters_filenames = self.get_sorted_chapters()
        read_chapters = []
        for file in chapters_filenames:
            with open(f"{self.path}/{file}", "r") as f:
                read_chapters.append(self._list_to_string(f.readlines()))
        return self._list_to_string(read_chapters)

    def read_chapters(self, chapters_filenames: list) -> str:
        read_chapters = []
        for file in chapters_filenames:
            with open(f"{self.path}/{file}", "r") as f:
                read_chapters.append(self._list_to_string(f.readlines()))
        return self._list_to_string(read_chapters)

    def get_sorted_chapters(self) -> list:
        manuscript = os.listdir(self.path)
        return sorted([file for file in manuscript if re.match(r"\d\d_.*\.md|\d\d_.*\.txt", file)])

    def _list_to_string(self, list: list) -> str:
        return "".join(list)
