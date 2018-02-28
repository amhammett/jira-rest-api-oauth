.PHONY: help test flake8 isort venv install

ifeq ($(OS),Windows_NT)
    python_path := $(shell where python)
    venv_flake8_path := venv\Scripts\flake8
    venv_isort_path := venv\Scripts\isort
    venv_pip_path := venv\Scripts\pip
    venv_python_path := venv\Script\python
    virtualenv_path := python -m virtualenv
else
    python_path := $(shell which python2.7)
    venv_flake8_path := ./venv/bin/flake8
    venv_isort_path := ./venv/bin/isort
    venv_pip_path := ./venv/bin/pip
    venv_python_path := venv/bin/python
    virtualenv_path := virtualenv
endif

help: ## this help task
	@echo 'Available targets'
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

# environment
venv: ## virtual environment
	$(virtualenv_path) venv --python=$(python_path)

install: ## install all the things
	$(venv_pip_path) install -r requirements.txt

# development
generate-rsa: ## generate rsa private/public keys
	openssl genrsa -out rsa.pem 1024
	openssl rsa -in rsa.pem -pubout -out rsa.pub

oauth-dance: ## generate oauth tokens
	$(venv_python_path) ./src/oauth-dance.py --jira-server=$(jira-server)

oauth-jira-projects: ## query jira for projects
	$(venv_python_path) ./src/oauth-jira-projects.py --jira-server=$(jira-server) --token=$(token) --token-secret=$(token-secret)

# test
test: | isort flake8 ## test all the things

flake8:
	$(venv_flake8_path) src/

isort:
	$(venv_isort_path) --quiet --check-only --recursive src
