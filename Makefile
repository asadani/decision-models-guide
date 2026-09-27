# Makefile: build pipeline for "Decision Models"
#
#   make pdf         screen PDF (11pt, oneside)
#   make paperback   6x9 interior PDF (twoside, KDP-style margins)
#   make diagrams    render assets/diagrams/src/*.tex to PNG
#   make manuscript  concatenate book/ into output/manuscript.md
#   make verify      check every URL in book/ returns 2xx/3xx
#   make clean       remove output/ and generated diagrams

SHELL := /usr/bin/env bash

TITLE        := decision-models
OUTPUT_DIR   := output
BUILD_DIR    := build
SCRIPTS_DIR  := scripts
MANUSCRIPT   := $(OUTPUT_DIR)/manuscript.md
PDF_OUT      := $(OUTPUT_DIR)/$(TITLE).pdf
PAPERBACK_OUT := $(OUTPUT_DIR)/$(TITLE)-paperback-interior.pdf
METADATA     := $(BUILD_DIR)/metadata.yaml
PAPERBACK_METADATA := $(BUILD_DIR)/metadata-paperback.yaml

PANDOC       := pandoc
PANDOC_FROM  := markdown+footnotes+yaml_metadata_block+pipe_tables+raw_tex+raw_html+task_lists+smart
# pandoc separates --resource-path entries with ';' on Windows and ':' elsewhere.
# A wrong separator also corrupts the TEXINPUTS it hands to pdflatex.
ifeq ($(OS),Windows_NT)
  PATHSEP := ;
else
  PATHSEP := :
endif
RESOURCE_PATH := .$(PATHSEP)assets$(PATHSEP)$(OUTPUT_DIR)
COMMON_FLAGS := --from $(PANDOC_FROM) --toc --toc-depth=2 "--resource-path=$(RESOURCE_PATH)" --lua-filter=$(BUILD_DIR)/chapter-headings.lua
PDF_ENGINE   := pdflatex

.PHONY: all pdf paperback diagrams manuscript verify preflight clean

all: preflight diagrams pdf paperback

pdf: preflight $(PDF_OUT)
paperback: preflight $(PAPERBACK_OUT)

preflight:
	@bash $(SCRIPTS_DIR)/preflight.sh

diagrams:
	@python $(SCRIPTS_DIR)/render_diagrams.py

verify:
	@bash $(SCRIPTS_DIR)/verify-links.sh

manuscript: $(MANUSCRIPT)

$(MANUSCRIPT): book/00-front-matter/*.md book/01-chapters/*.md book/02-appendices/*.md
	@bash $(SCRIPTS_DIR)/concat-chapters.sh

COVER_PNG    := assets/cover/decision-models-front-cover.png

$(PDF_OUT): $(MANUSCRIPT) $(METADATA) $(BUILD_DIR)/frontcover.tex $(COVER_PNG)
	@echo "build: pandoc -> pdf (with front cover)"
	@$(PANDOC) $(MANUSCRIPT) $(COMMON_FLAGS) --metadata-file=$(METADATA) \
		--include-before-body=$(BUILD_DIR)/frontcover.tex \
		--pdf-engine=$(PDF_ENGINE) -o $(PDF_OUT)

$(PAPERBACK_OUT): $(MANUSCRIPT) $(PAPERBACK_METADATA)
	@echo "build: pandoc -> paperback interior pdf (6x9, twoside)"
	@$(PANDOC) $(MANUSCRIPT) $(COMMON_FLAGS) --metadata-file=$(PAPERBACK_METADATA) \
		--pdf-engine=$(PDF_ENGINE) -o $(PAPERBACK_OUT)

clean:
	@rm -rf $(OUTPUT_DIR) assets/diagrams/generated/*.png
	@echo "clean: OK"
