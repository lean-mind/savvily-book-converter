import subprocess as sp
import re


class BasicFormatter:
    formatted_manuscript: str

    def __init__(self, raw_manuscript: str):
        self.raw_manuscript = raw_manuscript

    def check_links(self):
        self.formatted_manuscript = self.raw_manuscript.replace("] (", "](")

    def check_references(self):
        self.formatted_manuscript = self.raw_manuscript.replace(" [", "[")

    def check_headings(self):
        self.formatted_manuscript = self.raw_manuscript.replace("\n#", "\n\n#")

    def check_lang_tags(self):
        def format_and_capitalize(match):
            code_block_tag = match.group(1)
            capitalized_lang_tag = match.group(2).capitalize()
            return code_block_tag + r"{title=" + capitalized_lang_tag + r"}"

        code_block_tag_expression = r"(```)(.+)$"
        self.formatted_manuscript = re.sub(
            code_block_tag_expression, format_and_capitalize, self.raw_manuscript
        )

    def output(self):
        return self.formatted_manuscript


def run(input_markdown_path: str):
    find_command = [
        "find",
        input_markdown_path,
        "-maxdepth",
        "1",
        "-name",
        "[0-9]*.txt",
        "-o",
        "-name",
        "[0-9]*.md",
    ]
    unsorted_manuscript = sp.Popen(find_command, stdout=sp.PIPE).stdout

    sort_command = ["sort", "-V"]
    sorted_manuscript = sp.Popen(
        sort_command, stdin=unsorted_manuscript, stdout=sp.PIPE
    ).stdout

    cat_to_stdout = ["xargs", "cat"]
    manuscript_stream = sp.Popen(
        cat_to_stdout, stdin=sorted_manuscript, stdout=sp.PIPE
    ).stdout

    return sp.Popen(
        __build_sed_command(), stdin=manuscript_stream, stdout=sp.PIPE
    ).stdout


def __build_sed_command() -> list:
    insert_line_before_headers = r"s:(^#):\n\1:"
    remove_space_from_link_tags = r"s:] \(:](:g"
    capitalize_code_block_languages = r"s:(```)(.+)$:\1{title=\u\2}:"
    remove_space_before_anchor = r"s:\s\[\^:\[\^:g"
    return [
        "sed",
        "-Ee",
        insert_line_before_headers,
        "-Ee",
        remove_space_from_link_tags,
        "-Ee",
        capitalize_code_block_languages,
        "-Ee",
        remove_space_before_anchor,
    ]
