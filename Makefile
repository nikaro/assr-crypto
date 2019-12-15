.PHONY: all
all:

.PHONY: install
install:
	@echo "Installing..."
	@bundle

.PHONY: render
render:
	@echo "Rendering..."
	@bundle exec asciidoctor-revealjs index.adoc

.PHONY: serve
serve:
	@echo "Serving..."
	@python3 -m http.server
