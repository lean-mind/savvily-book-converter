FROM pandoc/latex:latest

# Install latex libraries & dependencies
RUN tlmgr update --self \
  && tlmgr install \
    pdfpages \
    tocloft  \
    emptypage  \
    footmisc  \
    titlesec  \
    wallpaper  \
    roboto  \
    incgraph  \
    tcolorbox  \
    environ  \
    eso-pic \
    datatool
RUN apk add sed ghostscript curl

# Install fonts
RUN /bin/sh -c \
  "$(curl -fsSL https://raw.githubusercontent.com/JetBrains/JetBrainsMono/master/install_manual.sh)" \
  && cp /root/.local/share/fonts/fonts/ttf/* /usr/share/fonts \
  && curl -L -O https://github.com/googlefonts/roboto/releases/download/v2.138/roboto-unhinted.zip \
  && unzip -q roboto-unhinted.zip -d /usr/share/fonts

# Clean font cache
RUN fc-cache -f && rm -rf /var/cache/*

ENTRYPOINT ["sh", "-c"]
