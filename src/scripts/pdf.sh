#!/bin/sh
. ./src/scripts/manuscriptFormatter.sh

outputType=$1
latexClass=$2

mkdir -p output/.tmp && cd .tmp-manuscript || exit

formattedManuscript=$(manuscriptFormatter "$outputType")

# Process main section
echo "$formattedManuscript" | pandoc \
    --pdf-engine=xelatex \
    --template=../src/templates/"$outputType"/custom-"$latexClass".tex \
    --listings \
    -V documentclass="$latexClass" \
    -f markdown-implicit_figures \
    -o ./../output/.tmp/tmp_book_for_"$outputType".pdf && \

# Process book opening section
xelatex -output-directory ./../output/.tmp ../src/templates/"$outputType"/opening.tex && \

# Join opening and main section
gs \
    -q \
    -dNOPAUSE \
    -dBATCH \
    -sDEVICE=pdfwrite \
    -sOutputFile=./../output/book_for_"$outputType".pdf \
    ./../output/.tmp/opening.pdf ./../output/.tmp/tmp_book_for_"$outputType".pdf && \

rm -rf ../output/.tmp && \

echo "PDF for $outputType successfully generated"
