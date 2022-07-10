from formatter.ManuscriptReader import ManuscriptReader


reader = ManuscriptReader()


class TestReader:
    def test_files_are_sorted(self):
        sorted_chapters = reader.get_sorted_chapters("sample-manuscript")
        expected_files = ["01_chapter.md", "02_chapter.md"]
        assert sorted_chapters == expected_files
