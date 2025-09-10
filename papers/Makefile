# Makefile for Pipeline & Peril Academic Papers
# Generates PDF from LaTeX sources

.PHONY: all pdf clean view

# LaTeX compiler configuration
LATEX = pdflatex
BIBTEX = bibtex
LATEX_FLAGS = -interaction=nonstopmode -halt-on-error

# Main paper
PAPER = main-paper
TEX_FILE = $(PAPER).tex
PDF_FILE = $(PAPER).pdf

# Build PDF
all: pdf

pdf: $(PDF_FILE)

$(PDF_FILE): $(TEX_FILE) references.bib
	@echo "Building LaTeX paper..."
	$(LATEX) $(LATEX_FLAGS) $(TEX_FILE)
	$(BIBTEX) $(PAPER)
	$(LATEX) $(LATEX_FLAGS) $(TEX_FILE)
	$(LATEX) $(LATEX_FLAGS) $(TEX_FILE)
	@echo "PDF generated: $(PDF_FILE)"

# View the PDF
view: $(PDF_FILE)
	@if command -v open >/dev/null 2>&1; then \
		open $(PDF_FILE); \
	elif command -v xdg-open >/dev/null 2>&1; then \
		xdg-open $(PDF_FILE); \
	else \
		echo "Please open $(PDF_FILE) manually"; \
	fi

# Clean auxiliary files
clean:
	rm -f *.aux *.log *.bbl *.blg *.out *.toc *.lof *.lot
	rm -f *.fls *.fdb_latexmk *.synctex.gz

# Deep clean (including PDF)
distclean: clean
	rm -f $(PDF_FILE)

# Check LaTeX installation
check:
	@command -v $(LATEX) >/dev/null 2>&1 && echo "✓ pdflatex found" || echo "✗ pdflatex not found"
	@command -v $(BIBTEX) >/dev/null 2>&1 && echo "✓ bibtex found" || echo "✗ bibtex not found"

help:
	@echo "Available targets:"
	@echo "  make pdf     - Generate PDF from LaTeX source"
	@echo "  make view    - Open generated PDF"
	@echo "  make clean   - Remove auxiliary files"
	@echo "  make check   - Check LaTeX installation"
	@echo "  make help    - Show this message"