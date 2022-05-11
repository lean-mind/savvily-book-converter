def getCommandFor(type: str):
  sortedManuscript = "find . -maxdepth 1 -name '[0-9]*.txt' -o -name '[0-9]*.md' | sort -V | xargs cat"
  formattedManuscript = r"sed -Ee 's:(^#):\n\1:' -Ee 's:] \(:](:g' -Ee 's:(```)(.+)$:\1{title=\u\2}:' -Ee 's:\s\[\^:\[\^:g'"

  if type == "print":
      formattedManuscript = r'%s | sed -E "/!.*/! s:(.+?)\[(.....+?)\]\(([^)]+)\)(.+?):\1\2[^\3]\4\n\n[^\3]\: \3\n:g' % (formattedManuscript)

  return '%s | %s' % (sortedManuscript, formattedManuscript)
