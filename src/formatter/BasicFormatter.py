import subprocess as sp


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
