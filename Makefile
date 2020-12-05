.PHONY: all
all:

.PHONY: setup
## setup: Installs required Gems
setup:
	@echo "Installing..."
	@command -v netlify || npm install --global netlify-cli
	@command -v asciidoctor-revealjs || npm install --global @asciidoctor/core @asciidoctor/reveal.js

.PHONY: build
## build: Renders the asciidoc file to HTML
build:
	@echo "Rendering..."
	@asciidoctor-revealjs --attribute revealjsdir=https://cdn.jsdelivr.net/npm/reveal.js@3.9.2 --out-file output/index.html index.adoc

.PHONY: serve
## serve: Serves the content on port 8000
serve:
	@echo "Serving..."
	@python3 -m http.server

.PHONY: deploy
## deploy: Deploy to Netlify
deploy:
	@echo "Uploading..."
	@netlify deploy --dir=output --prod --build

.PHONY: help
## help: Prints this help message
help:
	@echo -e "Usage: \n"
	@sed -n 's/^##//p' ${MAKEFILE_LIST} | column -t -s ':' |  sed -e 's/^/ /'
