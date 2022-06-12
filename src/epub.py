import subprocess
import sys
from os import makedirs, chdir
from typing import IO
from manuscriptFormatter import get_formatted_manuscript_stream_for_epub
from typing import Union


def __build_pandoc_command() -> list:
    metadata = '--metadata-file=../src/templates/epub/metadata.yml'
    output = '--output=./../output/ebook.epub'
    css = '--css=../src/templates/epub/epub.css'
    cover_image = '--epub-cover-image=./resources/book-cover-print.png'
    font = '--epub-embed-font=/usr/share/fonts/Roboto-Bold.ttf'
    return ['timeout', '600', 'pandoc', font, css, cover_image, output, metadata]


def __create_epub_from_stream(formatted_stream: Union[IO[bytes], None]):
    subprocess.run(__build_pandoc_command(), stdin=formatted_stream, check=True)


if __name__ == "__main__":
    try:
        makedirs('output', exist_ok=True)
        chdir('.tmp-manuscript')
        __create_epub_from_stream(get_formatted_manuscript_stream_for_epub())
        sys.exit(0)
    except subprocess.CalledProcessError as e:
        print('[ERROR]: Pandoc command failed!\n', e)
        sys.exit(1)
    except Exception as e:
        print('[ERROR]: Something went wrong!\n', e)
        sys.exit(1)
