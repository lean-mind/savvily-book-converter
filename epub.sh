#!/bin/sh

cd codigo-sostenible/manuscript

# Prepare markdown for processing

# Sort all chapters and cat them to stdout
find . -name "[0-9]*.txt" | sort -V | xargs  cat |\

# Ensure: h1 headers work, links respect md format, code block languages are passed as capitalized titles
sed -Ee 's:(^#):\n\1:' \
    -Ee 's:] \(:](:g' \
    -Ee 's:(```)(.+)$:\1{title=\u\2}:' |\

# Run Pandoc on stdin
pandoc \
    --toc                                                 \
    --css ../../epub.css                                  \
    --epub-cover-image ./resources/Codigo_Sostenible.png  \
    -o ./../../output/ebook.epub                          \
    ../../metadata.yml                                    \
&& echo "EPUB successfully generated"
