import subprocess
import sys
from os import makedirs, chdir
import formatter.ScreenPDFFormatter as screenPdfFormatter


def __pandoc_command(manuscript_path: str) -> list:
    engine = "--pdf-engine=xelatex"
    template = "--template=src/templates/screen/custom-report.tex"
    figures = "markdown-implicit_figures"
    resources = f"--resource-path={manuscript_path}"
    output = ".tmp-manuscript/chapters.pdf"
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
        resources,
    ]


def __compile_chapters(manuscript_path: str):
    formatted_stream = screenPdfFormatter.run(manuscript_path)
    subprocess.run(
        __pandoc_command(manuscript_path), stdin=formatted_stream, check=True
    )


# TODO.maybe replace xelatex? no way to avoid cd and mkdir
def __compile_opnening():
    xelatex_command = [
        "xelatex",
        "-output-directory",
        ".",
        "../src/templates/screen/opening.tex",
    ]
    chdir(".tmp-manuscript")
    subprocess.run(xelatex_command)
    chdir("../")


def __join_sections(output_name: str):
    output = f"-sOutputFile=output/{output_name}.pdf"
    ghostscript_command = [
        "gs",
        "-q",
        "-dNOPAUSE",
        "-dBATCH",
        "-sDEVICE=pdfwrite",
        output,
        ".tmp-manuscript/opening.pdf",
        ".tmp-manuscript/chapters.pdf",
    ]
    subprocess.run(ghostscript_command)


def __compile_pdf_from(manuscript_path: str):
    __compile_chapters(manuscript_path)
    __compile_opnening()
    __join_sections("python_screen")


if __name__ == "__main__":
    try:
        makedirs("output", exist_ok=True)
        manuscript_path = sys.argv[1]
        __compile_pdf_from(manuscript_path)
        sys.exit(0)
    except subprocess.CalledProcessError as e:
        print("[ERROR]: Pandoc command failed!\n", e)
        sys.exit(1)
    except Exception as e:
        print("[ERROR]: Something went wrong!\n", e)
        sys.exit(1)
