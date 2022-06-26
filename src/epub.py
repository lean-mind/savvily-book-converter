import subprocess
import sys
from os import makedirs
from manuscriptFormatter import get_formatted_manuscript_stream_for_epub


def __build_pandoc_command(manuscript_path: str) -> list:
    metadata = "--metadata-file=src/templates/epub/metadata.yml"
    resources = f"--resource-path={manuscript_path}"
    output = "--output=output/ebook.epub"
    css = "--css=src/templates/epub/epub.css"
    cover_image = f"--epub-cover-image={manuscript_path}/resources/book-cover-print.png"
    font = "--epub-embed-font=/usr/share/fonts/Roboto-Bold.ttf"
    return ["timeout", "600", "pandoc", font, css, cover_image, output, metadata, resources]


def __create_epub_from_stream(manuscript_path: str):
    formatted_stream = get_formatted_manuscript_stream_for_epub(manuscript_path)
    subprocess.run(__build_pandoc_command(manuscript_path), stdin=formatted_stream, check=True)


if __name__ == "__main__":
    try:
        makedirs("output", exist_ok=True)
        manuscript_path = sys.argv[1]
        __create_epub_from_stream(manuscript_path)
        sys.exit(0)
    except subprocess.CalledProcessError as e:
        print("[ERROR]: Pandoc command failed!\n", e)
        sys.exit(1)
    except Exception as e:
        print("[ERROR]: Something went wrong!\n", e)
        sys.exit(1)
