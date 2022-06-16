import subprocess as sp
from typing import IO
from typing import Union


def get_formatted_manuscript_stream_for_epub() -> Union[IO[bytes], None]:
    return __basic_formatted_stream()


def get_formatted_manuscript_stream_for_screen_pdf() -> Union[IO[bytes], None]:
    return __basic_formatted_stream()


def get_formatted_manuscript_stream_for_print_pdf() -> Union[IO[bytes], None]:
    ignore_images = r"/!.*/!"
    search = __build_search_regex()
    replace = __build_replace_regex()
    turn_links_to_footnotes = f'sed -E "{ignore_images} s:{search}:{replace}:g"'
    return sp.Popen(
        turn_links_to_footnotes,
        stdin=__basic_formatted_stream(),
        stdout=sp.PIPE,
        shell=True,
    ).stdout


def __build_search_regex() -> str:
    group_preceding_link = r"(.+?)"
    group_link_text = r"\[(.....+?)\]"
    group_link_url = r"\(([^)]+)\)"
    group_following_link = r"(.+?)"
    return (
        f"{group_preceding_link}{group_link_text}{group_link_url}{group_following_link}"
    )


def __build_replace_regex() -> str:
    preceding_reference = r"\1"
    referenced_text = r"\2"
    url_as_anchor_text = r"\3"
    following_reference = r"\4"
    return f"{preceding_reference}{referenced_text}[^{url_as_anchor_text}]{following_reference}\\n\\n[^{url_as_anchor_text}]\\: {url_as_anchor_text}\\n"


def __basic_formatted_stream() -> Union[IO[bytes], None]:
    find_command = [
        "find",
        ".",
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
