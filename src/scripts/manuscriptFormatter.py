import subprocess


def getCommandFor(type: str):
  sortCommand = "find . -maxdepth 1 -name '[0-9]*.txt' -o -name '[0-9]*.md' | sort -V | xargs cat"
  formatCommand = r"sed -Ee 's:(^#):\n\1:' -Ee 's:] \(:](:g' -Ee 's:(```)(.+)$:\1{title=\u\2}:' -Ee 's:\s\[\^:\[\^:g'"

  if type == "print":
    linksAsFootnotes = r'sed -E "/!.*/! s:(.+?)\[(.....+?)\]\(([^)]+)\)(.+?):\1\2[^\3]\4\n\n[^\3]\: \3\n:g'
    formatCommand = r'%s | %s' % (formatCommand, linksAsFootnotes)

  command = '%s | %s' % (sortCommand, formatCommand)
  return subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
