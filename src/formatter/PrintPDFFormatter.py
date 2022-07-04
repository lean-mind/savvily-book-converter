import subprocess as sp
import src.formatter.BasicFormatter as bf


def run(input_markdown_path: str):
    ignore_images = r"/!.*/!"
    search = __build_search_regex()
    replace = __build_replace_regex()
    turn_links_to_footnotes = f'sed -E "{ignore_images} s:{search}:{replace}:g"'
    return sp.Popen(
        turn_links_to_footnotes,
        stdin=bf.run(input_markdown_path),
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
