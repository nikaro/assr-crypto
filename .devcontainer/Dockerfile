FROM nikaro/debian-dev

# avoid warnings by switching to noninteractive
ENV DEBIAN_FRONTEND=noninteractive

RUN \
    # install required tools
    sudo apt-get update && \
    sudo apt-get install -y \
        asciidoctor \
	ruby-bundler \
        && \
    # clean up
    sudo apt-get autoremove -y && \
    sudo apt-get clean -y && \
    sudo rm -rf /var/lib/apt/lists/* &&  \
    :

# switch back to dialog for any ad-hoc use of apt-get
ENV DEBIAN_FRONTEND=dialog
