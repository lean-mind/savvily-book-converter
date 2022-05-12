import subprocess
import sys
import os
import manuscriptFormatter

subprocess.run(['mkdir', '-p', 'output'])
os.chdir('.tmp-manuscript')

formattingCommand = manuscriptFormatter.getFormattedManuscriptStreamFor("ebook")

pandocEpubCommand = 'timeout 600 pandoc --epub-embed-font=/usr/share/fonts/Roboto-Bold.ttf --css ../src/templates/epub/epub.css --epub-cover-image ./resources/book-cover-print.png -o ./../output/ebook.epub --metadata-file ../src/templates/epub/metadata.yml'
try:
    subprocess.run(pandocEpubCommand, stdin=formattingCommand, check=True, shell=True)
    sys.exit(0)
except subprocess.CalledProcessError as e:
    print('[ERROR]:', e)
    sys.exit(1)
