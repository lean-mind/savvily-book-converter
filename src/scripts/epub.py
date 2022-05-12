import subprocess
import sys
import os
import manuscriptFormatter


def buildPandocCommand():
    metadata = '--metadata-file=../src/templates/epub/metadata.yml'
    output = '--output=./../output/ebook.epub'
    css = '--css=../src/templates/epub/epub.css'
    coverImage = '--epub-cover-image=./resources/book-cover-print.png'
    font = '--epub-embed-font=/usr/share/fonts/Roboto-Bold.ttf'
    return ['timeout', '600', 'pandoc', font, css, coverImage, output, metadata]


def createEpubFromStream(formattedStream):
    subprocess.run(buildPandocCommand(), stdin=formattedStream, check=True)


if __name__ == "__main__":
    try:
        os.makedirs('output', exist_ok=True)
        os.chdir('.tmp-manuscript')
        createEpubFromStream(manuscriptFormatter.getFormattedManuscriptStreamFor("ebook"))
        sys.exit(0)
    except subprocess.CalledProcessError as e:
        print('[ERROR]: Pandoc command failed!\n', e)
        sys.exit(1)
    except Exception as e:
        print('[ERROR]: Something went wrong!\n', e)
        sys.exit(1)
