.PHONY: all
all: install serve

.PHONY: install
## install: Installs required Gems
install:
	@echo "Installing..."
	@bundle

.PHONY: render
## render: Renders the asciidoc file to HTML
render:
	@echo "Rendering..."
	@bundle exec asciidoctor-revealjs index.adoc

.PHONY: serve
## serve: Serves the content on http://localhost:8000
serve:
	@echo "Serving..."
	@python3 -m http.server

.PHONY: help
## help: Prints this help message
help:
	@echo "Usage: \n"
	@sed -n 's/^##//p' ${MAKEFILE_LIST} | column -t -s ':' |  sed -e 's/^/ /'
