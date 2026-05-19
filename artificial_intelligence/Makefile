.PHONY: build clean show

build:
	@echo "Building the LaTeX document..."
	@latexmk -pdf main.tex

clean:
	@echo "Removing all LaTeX auxiliary files..."
	@rm -f *.aux *.fdb_latexmk *.fls *.log *.out \
	  *.pdf *.gz indent.log *.bbl *.blg *\(busy\)
	@echo "Removed all LaTeX auxiliary files..."
