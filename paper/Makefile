# Build the paper PDF
.PHONY: all clean

all: paper.pdf

paper.pdf: paper.tex sections/*.tex figures/*.pdf references.bib npjcm.sty
	latexmk -pdf -pdflatex="pdflatex -interaction=nonstopmode" paper.tex

clean:
	latexmk -c paper.tex
	rm -f paper.bbl paper.run.xml
