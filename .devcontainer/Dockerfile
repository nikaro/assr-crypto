FROM nikaro/debian-dev

# avoid warnings by switching to noninteractive
ENV DEBIAN_FRONTEND=noninteractive

RUN \
    # install required tools
    curl -sL https://deb.nodesource.com/setup_lts.x | sudo -E bash - && \
    sudo apt-get install -y \
	nodejs \
        && \
    # clean up
    sudo apt-get autoremove -y && \
    sudo apt-get clean -y && \
    sudo rm -rf /var/lib/apt/lists/* &&  \
    # update npm
    npm config set prefix ~/.local && \
    npm install --global npm && \
    npm install --global \
        netlify-cli \
        @asciidoctor/core \
        @asciidoctor/reveal.js \
        && \
    :

# switch back to dialog for any ad-hoc use of apt-get
ENV DEBIAN_FRONTEND=dialog
