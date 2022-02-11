FROM pandoc/latex:latest

# Install latex libraries
    && tlmgr install pdfpages  \
    && tlmgr install tocloft  \
    && tlmgr install emptypage  \
    && tlmgr install footmisc  \
    && tlmgr install titlesec  \
    && tlmgr install wallpaper  \
    && tlmgr install roboto  \
    && tlmgr install incgraph  \
    && tlmgr install tcolorbox  \
    && tlmgr install environ  \
    && tlmgr install eso-pic
RUN apk add sed
RUN apk add ghostscript

# Install JetBrains Mono font
RUN mkdir -p /usr/share/fonts/
COPY src/JetBrains_Mono/static/*.ttf /usr/share/fonts/
COPY src/Roboto/*.ttf /usr/share/fonts/
RUN fc-cache -f && rm -rf /var/cache/*
ENTRYPOINT ["sh"]
