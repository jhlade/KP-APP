# APP Makefile
TARGET=app
DESKY_DIR=desky

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

cover: ## Tvorba desek (desky/app-desky.pdf), odděleně od hlavního dokumentu
	@cd ${DESKY_DIR} && ${TEX_BIN} ${TARGET}-desky

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
	@rm -f ${DESKY_DIR}/*.out ${DESKY_DIR}/*.log ${DESKY_DIR}/*.aux

clean: softclean ## Smazání dočasných souborů a produktů
	@rm -f *.pdf *.tar.gz *.zip
	@rm -f ${DESKY_DIR}/*.pdf

# app.tex je jediný dokument s \documentclass v kořeni - desky jsou
# v podadresáři ./desky, aby je Overleaf při importu nezvolil jako hlavní
# dokument místo app.tex
archive: all ## Vytvoření archivu ve formátu tar.gz
	@tar -czf ${TARGET}.tar.gz *.tex *.bib *.pdf Makefile ./struktura ./obrazky ./${DESKY_DIR}

archive-zip: all ## Vytvoření archivu ve formátu zip (pro nahrání do Overleaf)
	@zip -r ${TARGET}.zip *.tex *.bib *.pdf Makefile ./struktura ./obrazky ./${DESKY_DIR}
