import subprocess as sp


def getFormattedManuscriptStreamForEpub():
    return __basicFormattedStream()


def getFormattedManuscriptStreamForPrint():
    turnLinksToFootnotes = r'sed -E "/!.*/! s:(.+?)\[(.....+?)\]\(([^)]+)\)(.+?):\1\2[^\3]\4\n\n[^\3]\: \3\n:g'
    return sp.Popen(turnLinksToFootnotes, stdin=__basicFormattedStream(), stdout=sp.PIPE, shell=True).stdout



def __basicFormattedStream():
    findCommand = ["find", ".",
                   "-maxdepth", "1",
                   "-name", "[0-9]*.txt",
                   "-o",
                   "-name", "[0-9]*.md"]
    unsortedManuscript = sp.Popen(findCommand, stdout=sp.PIPE).stdout

    sortCommand = ["sort", "-V"]
    sortedManuscript = sp.Popen(sortCommand, stdin=unsortedManuscript, stdout=sp.PIPE).stdout

    catToStdout = ["xargs", "cat"]
    manuscriptStream = sp.Popen(catToStdout, stdin=sortedManuscript, stdout=sp.PIPE).stdout

    return sp.Popen(__buildSedCommand(), stdin=manuscriptStream, stdout=sp.PIPE).stdout


def __buildSedCommand():
    insertLineBeforeHeaders = "s:(^#):\\n\\1:"
    removeSpaceFromLinkTags = "s:] \\(:](:g"
    capitalizeCodeBlockLanguages = "s:(```)(.+)$:\\1{title=\\u\\2}:"
    removeSpaceBeforeAnchor = "s:\\s\\[\\^:\\[\\^:g"
    return ["sed",
            "-Ee", insertLineBeforeHeaders,
            "-Ee", removeSpaceFromLinkTags,
            "-Ee", capitalizeCodeBlockLanguages,
            "-Ee", removeSpaceBeforeAnchor]
