import subprocess


def getFormattedManuscriptStreamFor(type: str):
  findCommand = "find . -maxdepth 1 -name '[0-9]*.txt' -o -name '[0-9]*.md'"
  unsortedManuscript = subprocess.Popen(findCommand, stdout=subprocess.PIPE, shell=True).stdout

  sortCommand = "sort -V"
  sortedManuscript = subprocess.Popen(sortCommand, stdin=unsortedManuscript, stdout=subprocess.PIPE, shell=True).stdout

  turnToStreamCommand = "xargs cat"
  manuscriptStream = subprocess.Popen(turnToStreamCommand, stdin=sortedManuscript, stdout=subprocess.PIPE, shell=True).stdout

  fixHeaders = r"'s:(^#):\n\1:'"
  fixLinks = r"'s:] \(:](:g'"
  capitalizeCodeBlockLanguages = r"'s:(```)(.+)$:\1{title=\u\2}:'"
  fixAnchors = r"'s:\s\[\^:\[\^:g'"
  formatCommand = r"sed -Ee %s -Ee %s -Ee %s -Ee %s" % (fixHeaders, fixLinks, capitalizeCodeBlockLanguages, fixAnchors)
  formattedManuscriptStream = subprocess.Popen(formatCommand, stdin=manuscriptStream, stdout=subprocess.PIPE, shell=True).stdout

  if type == "print":
    linksAsFootnotes = r'sed -E "/!.*/! s:(.+?)\[(.....+?)\]\(([^)]+)\)(.+?):\1\2[^\3]\4\n\n[^\3]\: \3\n:g'
    return subprocess.Popen(linksAsFootnotes, stdin=formattedManuscriptStream, stdout=subprocess.PIPE, shell=True).stdout

  return formattedManuscriptStream
