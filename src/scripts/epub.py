import subprocess
import sys
import os
import manuscriptFormatter

subprocess.run(['mkdir', '-p', 'output'])
os.chdir('.tmp-manuscript')

formattingCommand = manuscriptFormatter.getCommandFor("ebook")

pandocEpubCommand = 'timeout 600 pandoc --epub-embed-font=/usr/share/fonts/Roboto-Bold.ttf --css ../src/templates/epub/epub.css --epub-cover-image ./resources/book-cover-print.png -o ./../output/ebook.epub --metadata-file ../src/templates/epub/metadata.yml'
subprocess.run(pandocEpubCommand, stdin=formattingCommand.stdout, shell=True)

sys.exit(0)
