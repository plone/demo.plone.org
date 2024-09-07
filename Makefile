### Defensive settings for make:
#     https://tech.davis-hansson.com/p/make/
SHELL:=bash
.ONESHELL:
.SHELLFLAGS:=-xeu -o pipefail -O inherit_errexit -c
.SILENT:
.DELETE_ON_ERROR:
MAKEFLAGS+=--warn-undefined-variables
MAKEFLAGS+=--no-builtin-rules

CURRENT_DIR:=$(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))


# We like colors
# From: https://coderwall.com/p/izxssa/colored-makefile-for-golang-projects
RED=`tput setaf 1`
GREEN=`tput setaf 2`
RESET=`tput sgr0`
YELLOW=`tput setaf 3`

.PHONY: all
all: build

# Add the following 'help' target to your Makefile
# And add help text after each target name starting with '\#\#'
.PHONY: help
help: ## This help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: install-frontend
install-frontend:  ## Install React Frontend
	$(MAKE) -C "./frontend/" install

.PHONY: build-frontend
build-frontend:  ## Build React Frontend
	$(MAKE) -C "./frontend/" build

.PHONY: start-frontend
start-frontend:  ## Start React Frontend
	$(MAKE) -C "./frontend/" start

.PHONY: install-backend
install-backend:  ## Create virtualenv and install Plone
	$(MAKE) -C "./backend/" build-dev
	$(MAKE) create-site

.PHONY: build-backend
build-backend:  ## Build Backend
	$(MAKE) -C "./backend/" build-dev

.PHONY: export-distribution
export-distribution: ## Export content
	$(MAKE) -C "./backend/" export-distribution

.PHONY: create-site
create-site: ## Create a Plone site with default content
	$(MAKE) -C "./backend/" create-site

.PHONY: start-backend
start-backend: ## Start Plone Backend
	$(MAKE) -C "./backend/" start

.PHONY: install
install:  ## Install
	@echo "Install Backend & Frontend"
	$(MAKE) install-backend
	$(MAKE) install-frontend
	$(MAKE) install-classic

# TODO production build

.PHONY: build
build:  ## Build in development mode
	@echo "Build"
	$(MAKE) build-backend
	$(MAKE) install-frontend
	$(MAKE) build-classic


.PHONY: start
start:  ## Start
	@echo "Starting application"
	$(MAKE) start-backend
	$(MAKE) start-frontend

.PHONY: clean
clean:  ## Clean installation
	@echo "Clean installation"
	$(MAKE) -C "./backend/" clean
	$(MAKE) -C "./frontend/" clean

.PHONY: format
format:  ## Format codebase
	@echo "Format codebase"
	$(MAKE) -C "./backend/" format
	$(MAKE) -C "./frontend/" format

.PHONY: i18n
i18n:  ## Update locales
	@echo "Update locales"
	$(MAKE) -C "./backend/" i18n
	$(MAKE) -C "./frontend/" i18n

.PHONY: test-backend
test-backend:  ## Test backend codebase
	@echo "Test backend"
	$(MAKE) -C "./backend/" test

.PHONY: test-frontend
test-frontend:  ## Test frontend codebase
	@echo "Test frontend"
	$(MAKE) -C "./frontend/" test

.PHONY: test
test:  test-backend test-frontend ## Test codebase

.PHONY: build-images
build-images:  ## Build docker images
	@echo "Build"
	$(MAKE) -C "./backend/" build-image
	$(MAKE) -C "./frontend/" build-image
	$(MAKE) -C "./classic/" build-image

## Classic

.PHONY: install-classic
install-classic:  ## Create virtualenv and install Plone
	$(MAKE) -C "./classic/" build-dev
	$(MAKE) create-site-classic

.PHONY: build-classic
build-classic:  ## Build classic
	$(MAKE) -C "./classic/" build-dev

.PHONY: export-distribution-classic
export-distribution-classic: ## Export content
	$(MAKE) -C "./classic/" export-distribution

.PHONY: create-site-classic
create-site-classic: ## Create a Plone site with default content
	$(MAKE) -C "./classic/" create-site

.PHONY: start-classic
start-classic: ## Start Plone Backend
	$(MAKE) -C "./classic/" start

## Docker stack
.PHONY: start-stack
start-stack:  ## Start local stack
	@echo "Start local Docker stack"
	@docker-compose -f devops/stacks/docker-compose-local.yml up -d --build

.PHONY: stop-stack
stop-stack:  ## Stop local stack
	@echo "Stop local Docker stack"
	@docker-compose -f devops/stacks/docker-compose-local.yml down
