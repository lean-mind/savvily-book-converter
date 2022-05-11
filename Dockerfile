FROM pandoc/latex:latest

# Install latex libraries
RUN tlmgr update --self \
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
    && tlmgr install eso-pic \
    && tlmgr install datatool
RUN apk add sed
RUN apk add ghostscript
RUN apk add python3

# Install JetBrains Mono font
RUN mkdir -p /usr/share/fonts/
COPY src/JetBrains_Mono/static/*.ttf /usr/share/fonts/
COPY src/Roboto/*.ttf /usr/share/fonts/
RUN fc-cache -f && rm -rf /var/cache/*
ENTRYPOINT ["sh"]
