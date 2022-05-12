import subprocess as sp


def getFormattedManuscriptStreamFor(type: str):
  findCommand = "find . -maxdepth 1 -name '[0-9]*.txt' -o -name '[0-9]*.md'"
  unsortedManuscript = sp.Popen(findCommand, stdout=sp.PIPE, shell=True).stdout

  sortCommand = ["sort", "-V"]
  sortedManuscript = sp.Popen(sortCommand, stdin=unsortedManuscript, stdout=sp.PIPE).stdout

  turnToStreamCommand = ["xargs", "cat"]
  manuscriptStream = sp.Popen(turnToStreamCommand, stdin=sortedManuscript, stdout=sp.PIPE).stdout

  fixHeaders = r"'s:(^#):\n\1:'"
  fixLinks = r"'s:] \(:](:g'"
  capitalizeCodeBlockLanguages = r"'s:(```)(.+)$:\1{title=\u\2}:'"
  fixAnchors = r"'s:\s\[\^:\[\^:g'"
  formatCommand = r"sed -Ee %s -Ee %s -Ee %s -Ee %s" % (fixHeaders, fixLinks, capitalizeCodeBlockLanguages, fixAnchors)
  formattedManuscriptStream = sp.Popen(formatCommand, stdin=manuscriptStream, stdout=sp.PIPE, shell=True).stdout

  if type == "print":
    linksAsFootnotes = r'sed -E "/!.*/! s:(.+?)\[(.....+?)\]\(([^)]+)\)(.+?):\1\2[^\3]\4\n\n[^\3]\: \3\n:g'
    return sp.Popen(linksAsFootnotes, stdin=formattedManuscriptStream.stdout, stdout=sp.PIPE, shell=True).stdout

  return formattedManuscriptStream
