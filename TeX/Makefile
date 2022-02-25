# APP Makefile

TEX_BIN=xelatex
BIB_BIN=biber

.PHONY: all

all: compile softclean

compile:
	${TEX_BIN} app
	${BIB_BIN} app
	${TEX_BIN} app
	${TEX_BIN} app

softclean:
	rm -f *.out *.bbl *.bcf *.dvi *.ps \
	*.log *.lof *.aux *.blg *.loa *.lot \
	*.toc *.run.xml

clean: softclean
	rm -f *.pdf
