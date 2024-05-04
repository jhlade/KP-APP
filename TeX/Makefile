# APP Makefile
TARGET=app

TEX_BIN=xelatex
BIB_BIN=biber

ifeq ($(OS),Windows_NT)
	OPEN_BIN = start \"\"
else
	UNAME_S := $(shell uname -s)
		ifeq ($(UNAME_S),Linux)
        	OPEN_BIN = xdg-open
    	endif
    	ifeq ($(UNAME_S),Darwin)
        	OPEN_BIN = open
    	endif
endif

.PHONY: all

all: cover compile softclean

cover:
	${TEX_BIN} ${TARGET}-desky

compile:
	${TEX_BIN} ${TARGET}
	${BIB_BIN} ${TARGET}
	${TEX_BIN} ${TARGET}
	${TEX_BIN} ${TARGET}
	
open:
	${OPEN_BIN} ${TARGET}.pdf

softclean:
	rm -f *.out *.bbl *.bcf *.dvi *.ps \
	*.log *.lof *.aux *.blg *.loa *.lot \
	*.toc *.apc *.run.xml

clean: softclean
	rm -f *.pdf *.tar.gz

archive: all
	tar -cf ${TARGET}.tar.gz *.tex *.bib *.pdf Makefile ./struktura ./obrazky
