.ONESHELL:

PATH_VENV := /tmp/centurion_erp

ACTIVATE_VENV :=. ${PATH_VENV}/bin/activate

.PHONY: clean prepare docs ansible-lint lint


prepare:
	git submodule update --init;
	git submodule foreach git submodule update --init;
	python3 -m venv ${PATH_VENV};
	${ACTIVATE_VENV};
	pip install -r website-template/gitlab-ci/mkdocs/requirements.txt;
	pip install -r gitlab-ci/lint/requirements.txt;
	pip install -r gitlab-ci/mkdocs/requirements.txt;
	pip install -r requirements.txt;
	pip install -r requirements_test.txt;
	npm install markdownlint-cli2;
	npm install markdownlint-cli2-formatter-junit;
	cp -f "website-template/.markdownlint.json" ".markdownlint.json";
	cp -f "gitlab-ci/lint/.markdownlint-cli2.jsonc" ".markdownlint-cli2.jsonc";


markdown-mkdocs-lint:
	PATH=${PATH}:node_modules/.bin markdownlint-cli2 "docs/*.md docs/**/*.md docs/**/**/*.md docs/**/**/**/*.md docs/**/**/**/**/**/*.md #CHANGELOG.md !gitlab-ci !website-template"


docs-lint: markdown-mkdocs-lint


docs: docs-lint
	${ACTIVATE_VENV}
	mkdocs build --clean



lint: markdown-mkdocs-lint


clean:
	rm -rf ${PATH_VENV}
	rm -rf pages
	rm -rf build
	rm -rf node_modules
	rm -f package-lock.json
	rm -f package.json