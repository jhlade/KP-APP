# APP Makefile
TARGET=app

TEX_BIN=xelatex
BIB_BIN=biber

.PHONY: all

all: cover compile softclean

cover:
	${TEX_BIN} ${TARGET}-desky

compile:
	${TEX_BIN} ${TARGET}
	${BIB_BIN} ${TARGET}
	${TEX_BIN} ${TARGET}
	${TEX_BIN} ${TARGET}

softclean:
	rm -f *.out *.bbl *.bcf *.dvi *.ps \
	*.log *.lof *.aux *.blg *.loa *.lot \
	*.toc *.apc *.run.xml

clean: softclean
	rm -f *.pdf
