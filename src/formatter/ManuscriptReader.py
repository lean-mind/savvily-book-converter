import os
import re


class ManuscriptReader:
    # def __init__(self):

    # def read(self):

    def get_sorted_chapters(self, path: str) -> list:
        dir_list = os.listdir(path)
        return sorted(
            [file for file in dir_list if re.match(r"\d\d_.*\.md|\d\d_.*\.txt", file)]
        )
