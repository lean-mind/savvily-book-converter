import subprocess as sp


def getFormattedManuscriptStreamForEpub():
    return basicFormattedStream()


def getFormattedManuscriptStreamForPrint():
    linksAsFootnotes = r'sed -E "/!.*/! s:(.+?)\[(.....+?)\]\(([^)]+)\)(.+?):\1\2[^\3]\4\n\n[^\3]\: \3\n:g'
    return sp.Popen(linksAsFootnotes, stdin=basicFormattedStream(), stdout=sp.PIPE, shell=True).stdout



def basicFormattedStream():
    findCommand = "find . -maxdepth 1 -name '[0-9]*.txt' -o -name '[0-9]*.md'"
    unsortedManuscript = sp.Popen(findCommand, stdout=sp.PIPE, shell=True).stdout

    sortCommand = ["sort", "-V"]
    sortedManuscript = sp.Popen(sortCommand, stdin=unsortedManuscript, stdout=sp.PIPE).stdout

    turnToStreamCommand = ["xargs", "cat"]
    manuscriptStream = sp.Popen(turnToStreamCommand, stdin=sortedManuscript, stdout=sp.PIPE).stdout

    return sp.Popen(buildSedCommand(), stdin=manuscriptStream, stdout=sp.PIPE, shell=True).stdout


def buildSedCommand():
    fixHeaders = r"'s:(^#):\n\1:'"
    fixLinks = r"'s:] \(:](:g'"
    capitalizeCodeBlockLanguages = r"'s:(```)(.+)$:\1{title=\u\2}:'"
    fixAnchors = r"'s:\s\[\^:\[\^:g'"
    return r"sed -Ee %s -Ee %s -Ee %s -Ee %s" % (fixHeaders, fixLinks, capitalizeCodeBlockLanguages, fixAnchors)
