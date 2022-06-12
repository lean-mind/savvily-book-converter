import subprocess
import sys
from os import makedirs, chdir
from io import BufferedReader
from manuscriptFormatter import getFormattedManuscriptStreamForEpub


def __buildPandocCommand() -> list:
    metadata = '--metadata-file=../src/templates/epub/metadata.yml'
    output = '--output=./../output/ebook.epub'
    css = '--css=../src/templates/epub/epub.css'
    coverImage = '--epub-cover-image=./resources/book-cover-print.png'
    font = '--epub-embed-font=/usr/share/fonts/Roboto-Bold.ttf'
    return ['timeout', '600', 'pandoc', font, css, coverImage, output, metadata]


def __createEpubFromStream(formattedStream: BufferedReader):
    subprocess.run(__buildPandocCommand(), stdin=formattedStream, check=True)


if __name__ == "__main__":
    try:
        makedirs('output', exist_ok=True)
        chdir('.tmp-manuscript')
        __createEpubFromStream(getFormattedManuscriptStreamForEpub())
        sys.exit(0)
    except subprocess.CalledProcessError as e:
        print('[ERROR]: Pandoc command failed!\n', e)
        sys.exit(1)
    except Exception as e:
        print('[ERROR]: Something went wrong!\n', e)
        sys.exit(1)
