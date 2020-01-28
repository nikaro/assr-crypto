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
## serve: Serves the content on port 8000
serve:
	@echo "Serving..."
	@python3 -m http.server

.PHONY: upload
## upload: Upload the content on the server
upload:
	@echo "Uploading..."
	@rsync -avzz . home.karolak.fr:/var/www/crypto/

.PHONY: help
## help: Prints this help message
help:
	@echo "Usage: \n"
	@sed -n 's/^##//p' ${MAKEFILE_LIST} | column -t -s ':' |  sed -e 's/^/ /'
