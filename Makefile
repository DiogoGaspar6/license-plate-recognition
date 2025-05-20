.DEFAULT_GOAL := help
.PHONY: tests
.SILENT:

include .env

## Colors
COLOR_RESET   = \033[0m
COLOR_INFO    = \033[32m
COLOR_COMMENT = \033[33m

PROJECT_NAME = 'license-plate-recognition'
NETWORK = 'license-plate-recognition'

## Help
help:
	printf "${COLOR_COMMENT}Usage:${COLOR_RESET}\n"
	printf " make [target]\n\n"
	printf "${COLOR_COMMENT}Available targets:${COLOR_RESET}\n"
	awk '/^[a-zA-Z\-\_0-9\.@]+:/ { \
		categoryMessage = match(lastLine, /^## \[(.*)\]/); \
		categoryLength = 0; \
		if (categoryMessage) { \
			categoryName = substr(lastLine, RSTART + 4, RLENGTH - 5); \
			categoryLength = length(categoryName) + 2; \
			if (!printedCategory[categoryName]) { \
				printedCategory[categoryName] = 1; \
				printf "\n${COLOR_COMMENT}%s:${COLOR_RESET}\n", categoryName; \
			} \
		} \
		helpMessage = match(lastLine, /^## (.*)/); \
		if (helpMessage) { \
			helpCommand = substr($$1, 0, index($$1, ":")); \
			helpMessage = substr(lastLine, RSTART + 3 + categoryLength, RLENGTH); \
			printf " ${COLOR_INFO}%-16s${COLOR_RESET} %s\n", helpCommand, helpMessage; \
		} \
	} \
	{ lastLine = $$0 }' $(MAKEFILE_LIST)

DOCKER_COMPOSE = docker compose --project-name $(PROJECT_NAME)
DOCKER_COMPOSE_EXEC ?= $(DOCKER_COMPOSE) exec

## [Docker] Start containers
up:
	$(DOCKER_COMPOSE) up -d

## [Docker] Stop containers
stop:
	$(DOCKER_COMPOSE) stop

## [Docker] Down containers
down:
	$(DOCKER_COMPOSE) down --remove-orphans --volumes

## [Docker] Build containers
build:
	$(DOCKER_COMPOSE) build

## [Docker] Get inside the container
shell sh:
	$(DOCKER_COMPOSE_EXEC) node-app /bin/sh

## [NPM] Install packages
install:
	$(DOCKER_COMPOSE_EXEC) pip install -r requirements.txt