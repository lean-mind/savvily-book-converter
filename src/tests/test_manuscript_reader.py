from formatter.ManuscriptReader import ManuscriptReader
import tests.expected_output_md as expected


reader = ManuscriptReader("sample-manuscript")


class TestReader:
    def test_files_are_sorted(self):
        sorted_chapters = reader.get_sorted_chapters()
        expected_files = ["01_chapter.md", "02_chapter.md"]
        assert sorted_chapters == expected_files

    def test_whole_manuscript_is_read(self):
        manuscript_content = reader.read()
        assert manuscript_content == expected.default

    def test_slected_chapters_are_read(self):
        selected_chapters = reader.read_chapters(["01_chapter.md"])
        assert selected_chapters == expected.ch_01
