import subprocess as sp


def getFormattedManuscriptStreamForEpub():
    return __basicFormattedStream()


def getFormattedManuscriptStreamForPrint():
    ignoreImages = r'/!.*/!'
    search = __buildSearchRegex()
    replace = __buildReplaceRegex()
    turnLinksToFootnotes = f'sed -E "{ignoreImages} s:{search}:{replace}:g"'
    print(turnLinksToFootnotes)
    return sp.Popen(turnLinksToFootnotes, stdin=__basicFormattedStream(), stdout=sp.PIPE, shell=True).stdout


def __buildSearchRegex():
    groupPrecedingLink = r'(.+?)'
    groupLinkText = r'\[(.....+?)\]'
    groupLinkUrl = r'\(([^)]+)\)'
    groupFollowingLink = r'(.+?)'
    return f'{groupPrecedingLink}{groupLinkText}{groupLinkUrl}{groupFollowingLink}'


def __buildReplaceRegex():
    precedingReference = r'\1'
    referencedText = r'\2'
    urlAsAnchorText = r'\3'
    followingReference = r'\4'
    return f'{precedingReference}{referencedText}[^{urlAsAnchorText}]{followingReference}\\n\\n[^{urlAsAnchorText}]\\: {urlAsAnchorText}\\n'


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
    insertLineBeforeHeaders = r"s:(^#):\n\1:"
    removeSpaceFromLinkTags = r"s:] \(:](:g"
    capitalizeCodeBlockLanguages = r"s:(```)(.+)$:\1{title=\u\2}:"
    removeSpaceBeforeAnchor = r"s:\s\[\^:\[\^:g"
    return ["sed",
            "-Ee", insertLineBeforeHeaders,
            "-Ee", removeSpaceFromLinkTags,
            "-Ee", capitalizeCodeBlockLanguages,
            "-Ee", removeSpaceBeforeAnchor]
