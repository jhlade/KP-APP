# APP Makefile
TARGET=app

TEX_BIN=xelatex
BIB_BIN=biber

ifeq ($(OS),Windows_NT)
	OPEN_BIN = start ""
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

all: cover compile softclean ## Překlad a vytvoření PDF (app.pdf)

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}'

cover: ## Tvorba desek (app-desky.pdf)
	@${TEX_BIN} ${TARGET}-desky

compile: ## Kompilace práce do PDF (app.pdf)
	@${TEX_BIN} ${TARGET}
	@${BIB_BIN} ${TARGET}
	@${TEX_BIN} ${TARGET}
	@${TEX_BIN} ${TARGET}
	
open: ## Otevřená výsledku v prohlížeči PDF
	${OPEN_BIN} ${TARGET}.pdf

softclean: ## Smazání dočasných souborů
	@rm -f *.out *.bbl *.bcf *.dvi *.ps \
	*.log *.lof *.aux *.blg *.loa *.lot \
	*.toc *.apc *.run.xml

clean: softclean ## Smazání dočasných souborů a produktů
	@rm -f *.pdf *.tar.gz *.zip

# app.tex jako hlavní dokument
TEX_FILES = ${TARGET}.tex $(filter-out ${TARGET}.tex,$(wildcard *.tex))

archive: all ## Vytvoření archivu ve formátu tar.gz
	@tar -czf ${TARGET}.tar.gz ${TEX_FILES} *.bib *.pdf Makefile ./struktura ./obrazky

archive-zip: all ## Vytvoření archivu ve formátu zip (pro nahrání do Overleaf)
	@zip -r ${TARGET}.zip ${TEX_FILES} *.bib *.pdf Makefile ./struktura ./obrazky
