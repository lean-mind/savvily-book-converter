import subprocess
import sys
import logging
from os import makedirs
import formatter.EpubFormatter as epubFormatter

logging.basicConfig(filename="logs.log", encoding="utf-8", level=logging.DEBUG)


def __pandoc_command(manuscript_path: str) -> list:
    metadata = "--metadata-file=src/templates/epub/metadata.yml"
    resources = f"--resource-path={manuscript_path}"
    output = "--output=output/ebook.epub"
    css = "--css=src/templates/epub/epub.css"
    cover_image = f"--epub-cover-image={manuscript_path}/resources/book-cover-print.png"
    font = "--epub-embed-font=/usr/share/fonts/Roboto-Bold.ttf"
    return [
        "timeout",
        "600",
        "pandoc",
        font,
        css,
        cover_image,
        output,
        metadata,
        resources,
    ]


def __compile_epub_from(manuscript_path: str):
    logging.info(" === COMPILING Epub ===")
    formatted_stream = epubFormatter.run(manuscript_path)
    subprocess.run(
        __pandoc_command(manuscript_path), stdin=formatted_stream, check=True
    )


if __name__ == "__main__":
    try:
        makedirs("output", exist_ok=True)
        manuscript_path = sys.argv[1]
        __compile_epub_from(manuscript_path)
        logging.info(" === DONE generating Epub ===")
        sys.exit(0)
    except subprocess.CalledProcessError as e:
        logging.error(f" === Pandoc command failed! === \n{e}")
        sys.exit(1)
    except Exception as e:
        logging.error(f" === Something went wrong! === \n{e}")
        sys.exit(1)
