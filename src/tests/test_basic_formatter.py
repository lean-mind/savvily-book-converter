from formatter.BasicFormatter import BasicFormatter


class TestBasicFormatter:
    def test_link_format(self):
        formatter = BasicFormatter("[this is some linked text] (this is a url)")
        formatter.check_links()
        actual_output = formatter.output()
        expected_output = "[this is some linked text](this is a url)"
        assert actual_output == expected_output

    def test_reference_format(self):
        formatter = BasicFormatter(" [^reference-text]:")
        formatter.check_references()
        actual_output = formatter.output()
        expected_output = "[^reference-text]:"
        assert actual_output == expected_output

    def test_headings_format(self):
        formatter = BasicFormatter("last paragraph.\n# New Chapter")
        formatter.check_headings()
        actual_output = formatter.output()
        expected_output = "last paragraph.\n\n# New Chapter"
        assert actual_output == expected_output

    def test_language_tags_format(self):
        formatter = BasicFormatter("```java")
        formatter.check_lang_tags()
        actual_output = formatter.output()
        expected_output = "```{title=Java}"
        assert actual_output == expected_output
