import subprocess


def getCommandFor(type: str):
  sortCommand = "find . -maxdepth 1 -name '[0-9]*.txt' -o -name '[0-9]*.md' | sort -V | xargs cat"
  manuscriptStream = subprocess.Popen(sortCommand, stdout=subprocess.PIPE, shell=True).stdout

  formatCommand = r"sed -Ee 's:(^#):\n\1:' -Ee 's:] \(:](:g' -Ee 's:(```)(.+)$:\1{title=\u\2}:' -Ee 's:\s\[\^:\[\^:g'"
  formattedManuscriptStream = subprocess.Popen(formatCommand, stdin=manuscriptStream, stdout=subprocess.PIPE, shell=True).stdout

  if type == "print":
    linksAsFootnotes = r'sed -E "/!.*/! s:(.+?)\[(.....+?)\]\(([^)]+)\)(.+?):\1\2[^\3]\4\n\n[^\3]\: \3\n:g'
    return subprocess.Popen(linksAsFootnotes, stdin=formattedManuscriptStream, stdout=subprocess.PIPE, shell=True).stdout

  return formattedManuscriptStream
