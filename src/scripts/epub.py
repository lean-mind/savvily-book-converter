import subprocess
import sys
import os

import manuscriptFormatter

formattingCommand = manuscriptFormatter.getCommandFor("ebook")

subprocess.run('mkdir -p output', capture_output=True, text=True, shell=True)
os.chdir('.tmp-manuscript')


pandocCommand = 'timeout 600 pandoc --epub-embed-font=/usr/share/fonts/Roboto-Bold.ttf --css ../src/templates/epub/epub.css --epub-cover-image ./resources/book-cover-print.png -o ./../output/ebook.epub --metadata-file ../src/templates/epub/metadata.yml'

paco = subprocess.run('%s | %s' % (formattingCommand, pandocCommand), capture_output=True, text=True, shell=True)

sys.exit(0)
