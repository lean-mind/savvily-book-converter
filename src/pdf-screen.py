import subprocess
import sys
from os import makedirs, chdir
from typing import IO
import manuscriptFormatter as formatter
from typing import Union


def __build_screen_pandoc_command() -> list:
    engine = "--pdf-engine=xelatex"
    template = "--template=../src/templates/screen/custom-report.tex"
    figures = "markdown-implicit_figures"
    output = "tmp_chapters.pdf"
    return [
        "timeout",
        "600",
        "pandoc",
        engine,
        template,
        "--listings",
        "-V",
        "documentclass=report",
        "-f",
        figures,
        "-o",
        output,
    ]


def __compile_screen_chapters(formatted_stream: Union[IO[bytes], None]):
    subprocess.run(__build_screen_pandoc_command(), stdin=formatted_stream, check=True)


def __compile_screen_opnening():
    xelatex_command = [
        "xelatex",
        "-output-directory",
        ".",
        "../src/templates/screen/opening.tex",
    ]
    subprocess.run(xelatex_command)


def __join_sections(output_name: str):
    output = f"-sOutputFile=./../output/{output_name}.pdf"
    ghostscript_command = [
        "gs",
        "-q",
        "-dNOPAUSE",
        "-dBATCH",
        "-sDEVICE=pdfwrite",
        output,
        "opening.pdf",
        "tmp_chapters.pdf",
    ]
    subprocess.run(ghostscript_command)


def __create_screen_pdf_from_stream(formatted_stream: Union[IO[bytes], None]):
    __compile_screen_chapters(formatted_stream)
    __compile_screen_opnening()
    __join_sections("screen_pdf_by_python")


if __name__ == "__main__":
    try:
        makedirs("output", exist_ok=True)
        chdir(".tmp-manuscript")
        __create_screen_pdf_from_stream(
            formatter.get_formatted_manuscript_stream_for_print_pdf()
        )
        sys.exit(0)
    except subprocess.CalledProcessError as e:
        print("[ERROR]: Pandoc command failed!\n", e)
        sys.exit(1)
    except Exception as e:
        print("[ERROR]: Something went wrong!\n", e)
        sys.exit(1)
