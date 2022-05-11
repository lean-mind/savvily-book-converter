#!/bin/sh
set -e

if [ $# -eq 1 ]; then
  if [ -d "./manuscript" ]; then
    manuscript="./manuscript"
  else
    echo "The manuscript folder doesn't exist"
    echo "The manuscript folder should contain a resources folder and files with .txt or .md extension \n"

    echo "Please place the manuscript folder in the project root \n"
    exit 1
  fi
elif [ $# -eq 2 ]; then
  manuscript=$2
else
    echo "Wrong input"
    exit 1
fi

case "$1" in
  -p| --print) scriptToRun="./src/scripts/pdf.sh print book" ;;

  -s| --screen) scriptToRun="./src/scripts/pdf.sh screen report" ;;

  #-e| --epub) scriptToRun="./src/scripts/epub.sh" format="epub";;
  -e| --epub) scriptToRun="-c python3 -B src/scripts/epub.py" format="epub";;

  -m| --mobi) scriptToRun="./src/scripts/mobi.sh";;

  -es | --epub-and-screen) ./convert.sh -e "$manuscript"; ./convert.sh -s "$manuscript"; exit ;;

  -a| --all) ./convert.sh -e "$manuscript"; ./convert.sh -p "$manuscript"; ./convert.sh -s "$manuscript" ; exit ;;

   *) printf "Unknown option %s\n" "$1" ; exit 1;;
esac

if [ -d .tmp-manuscript ]; then
  rm -rf .tmp-manuscript
fi

mkdir -p .tmp-manuscript && cp -r "$manuscript"/* ./.tmp-manuscript

docker run --rm \
  --volume "$PWD":/data \
  -u "$(id -u "$USER"):$(id -g "$USER")" \
  savvily-book-generator \
  $scriptToRun

rm -rf .tmp-manuscript

if [ "$format" = "epub" ]; then
  . ./src/scripts/epubFormatter.sh
fi

. ./src/scripts/wrapBooks.sh

